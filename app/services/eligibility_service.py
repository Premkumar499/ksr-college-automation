from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.database import Scholarship, EligibilityCheck
from app.schemas.scholarship import StudentCreate, EligibilityScholar


class EligibilityService:
    def __init__(self, db: Session):
        self.db = db

    def check_eligibility(
        self, student_data: StudentCreate, scholarship_ids: Optional[List[int]] = None
    ) -> List[EligibilityScholar]:
        """Check which scholarships a student is eligible for using Gemini LLM"""
        query = self.db.query(Scholarship)
        if scholarship_ids:
            query = query.filter(Scholarship.id.in_(scholarship_ids))
        scholarships = query.all()

        if not scholarships:
            return self._check_hardcoded_eligibility(student_data)

        import google.generativeai as genai
        from app.core.config import settings
        import json

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash", generation_config={"response_mime_type": "application/json"})

        scholarship_list = []
        for s in scholarships:
            scholarship_list.append({
                "id": s.id,
                "scheme_name": s.scheme_name,
                "criteria": s.eligibility_criteria,
                "category": s.category,
                "application_link": s.application_link
            })

        prompt = f"""You are an expert scholarship eligibility evaluator.
Given a student's profile and a list of internal scholarships with criteria, evaluate whether the student is eligible for EACH scholarship.
Output a JSON array where each item matches exactly this format:
{{
  "scholarship_id": <int>,
  "scholarship_name": "<string (use scheme_name)>",
  "eligibility_score": <int between 0 and 100>,
  "reasons": ["<string starting with ✓ if passing, or ❌ if failing>"]
}}
Score 100 if they technically meet all explicitly required criteria. 
Score 0 if they definitively fail a criteria (e.g. wrong gender, GPA below requirement, family income strictly higher than requirement).
Provide specific reasons referencing the student's metrics.

Student Profile:
{student_data.model_dump_json()}

Scholarships:
{json.dumps(scholarship_list)}
"""

        try:
            response = model.generate_content(prompt)
            results = json.loads(response.text)
            eligible = []
            for item in results:
                eligible.append(
                    EligibilityScholar(
                        scholarship_id=item.get("scholarship_id", 0),
                        scholarship_name=item.get("scholarship_name", "Unknown"),
                        eligibility_score=item.get("eligibility_score", 0),
                        reasons=item.get("reasons", []),
                    )
                )
            return sorted(eligible, key=lambda x: x.eligibility_score, reverse=True)
        except Exception as e:
            print(f"LLM Parsing error: {e}")
            return self._check_hardcoded_eligibility(student_data)

    def _check_hardcoded_eligibility(
        self, student: StudentCreate
    ) -> List[EligibilityScholar]:
        """Check eligibility using hardcoded scholarship rules"""
        results = []

        # SC | SCA | ST | SCC Scholarships
        if student.category and student.category.upper() in ["SC", "SCA", "ST", "SCC"]:
            score = 100
            reasons = ["✓ You belong to SC/SCA/ST/SCC category"]
            if student.family_income and student.family_income <= 250000:
                reasons.append("✓ Family income is below ₹2.5 Lakhs")
                score += 0
            else:
                reasons.append(
                    f"✗ Family income must be below ₹2.5 Lakhs (Your: {student.family_income or 'Not provided'})"
                )
                score -= 20

            results.append(
                EligibilityScholar(
                    scholarship_id=0,
                    scholarship_name="SC | SCA | ST | SCC Scholarships (Tamil Nadu)",
                    eligibility_score=min(score, 100),
                    reasons=reasons,
                )
            )

        # BC | MBC | DNC Scholarships
        if student.category and student.category.upper() in ["BC", "MBC", "DNC"]:
            score = 100
            reasons = ["✓ You belong to BC/MBC/DNC category"]
            if student.family_income and student.family_income <= 250000:
                reasons.append("✓ Family income is below ₹2.5 Lakhs")
            else:
                reasons.append(
                    f"✗ Family income must be below ₹2.5 Lakhs (Your: {student.family_income or 'Not provided'})"
                )
                score -= 30

            results.append(
                EligibilityScholar(
                    scholarship_id=0,
                    scholarship_name="BC | MBC | DNC Scholarships (Tamil Nadu)",
                    eligibility_score=min(score, 100),
                    reasons=reasons,
                )
            )

        # AICTE Scholarships
        if (
            student.year
            and student.year in [1, 2]
            and student.gpa
            and student.gpa >= 6.0
        ):
            reasons = ["✓ Enrolled in 1st or 2nd year technical course"]
            score = 80

            if student.family_income and student.family_income <= 800000:
                reasons.append("✓ Family income is below ₹8 Lakhs")
            else:
                reasons.append(
                    f"✗ Family income must be below ₹8 Lakhs (Your: {student.family_income or 'Not provided'})"
                )
                score -= 20

            if student.gender and student.gender.lower() == "female":
                results.append(
                    EligibilityScholar(
                        scholarship_id=0,
                        scholarship_name="AICTE – Pragati Scholarship (For Girls)",
                        eligibility_score=min(score, 100),
                        reasons=reasons + ["✓ You are a female student"],
                    )
                )

            results.append(
                EligibilityScholar(
                    scholarship_id=0,
                    scholarship_name="AICTE – Saksham Scholarship (For Specially Abled)",
                    eligibility_score=min(score - 30, 100),
                    reasons=reasons + ["Note: Requires 40%+ disability certificate"],
                )
            )

        # Private Scholarships
        if student.gpa and student.gpa >= 7.0:
            reasons = ["✓ GPA meets minimum requirement"]
            score = 100

            if student.department and any(
                dept in student.department.upper()
                for dept in ["CSE", "IT", "ECE", "EEE"]
            ):
                results.append(
                    EligibilityScholar(
                        scholarship_id=0,
                        scholarship_name="Aspire - Harihara Subramanian Scholarship",
                        eligibility_score=min(score, 100),
                        reasons=reasons
                        + ["✓ You are from eligible department (CSE/IT/ECE/EEE)"],
                    )
                )

        if student.family_income and student.family_income <= 1500000:
            results.append(
                EligibilityScholar(
                    scholarship_id=0,
                    scholarship_name="Reliance Foundation Undergraduate Scholarship",
                    eligibility_score=70 if student.family_income > 250000 else 100,
                    reasons=[
                        "✓ Family income meets requirement"
                        if student.family_income <= 1500000
                        else "✗ Income too high"
                    ],
                )
            )

        if (
            student.gender
            and student.gender.lower() == "female"
            and student.family_income
            and student.family_income <= 800000
        ):
            results.append(
                EligibilityScholar(
                    scholarship_id=0,
                    scholarship_name="Infosys Foundation STEM Stars Scholarship",
                    eligibility_score=80,
                    reasons=["✓ Female student", "✓ Income below ₹8 Lakhs"],
                )
            )

        return results

    def _evaluate_scholarship(
        self, scholarship: Scholarship, student: StudentCreate
    ) -> tuple[float, List[str]]:
        """Evaluate a single scholarship for a student"""
        score = 0.0
        reasons = []
        total_criteria = 0

        criteria = scholarship.eligibility_criteria or {}

        # Check GPA requirement
        if "min_gpa" in criteria:
            total_criteria += 1
            min_gpa = float(criteria["min_gpa"])
            if student.gpa and student.gpa >= min_gpa:
                score += 25
                reasons.append(f"✓ GPA {student.gpa} meets minimum {min_gpa}")
            else:
                reasons.append(
                    f"✗ GPA requirement: minimum {min_gpa} (your GPA: {student.gpa or 'not provided'})"
                )

        # Check category requirement
        if "category" in criteria:
            total_criteria += 1
            allowed_categories = [c.upper() for c in criteria["category"]]
            if student.category and student.category.upper() in allowed_categories:
                score += 25
                reasons.append(f"✓ Category '{student.category}' is eligible")
            else:
                reasons.append(f"✗ Category must be one of: {criteria['category']}")

        # Check family income
        if "max_income" in criteria:
            total_criteria += 1
            max_income = float(criteria["max_income"])
            if student.family_income and student.family_income <= max_income:
                score += 25
                reasons.append(
                    f"✓ Family income {student.family_income} is within limit {max_income}"
                )
            else:
                reasons.append(
                    f"✗ Income must be below {max_income} (your income: {student.family_income or 'not provided'})"
                )

        # Check year of study
        if "eligible_years" in criteria:
            total_criteria += 1
            eligible_years = criteria["eligible_years"]
            if student.year and student.year in eligible_years:
                score += 25
                reasons.append(f"✓ Year {student.year} is eligible")
            else:
                reasons.append(
                    f"✗ Only years {eligible_years} are eligible (your year: {student.year})"
                )

        # Check gender
        if "gender" in criteria:
            total_criteria += 1
            allowed_genders = [g.upper() for g in criteria["gender"]]
            if student.gender and student.gender.upper() in allowed_genders:
                score += 25
                reasons.append(f"✓ Gender '{student.gender}' is eligible")
            else:
                reasons.append(f"✗ Gender must be one of: {criteria['gender']}")

        # Calculate percentage score
        if total_criteria > 0:
            score = (score / (total_criteria * 25)) * 100
        else:
            score = 100  # No specific criteria, assume eligible

        return score, reasons

    def save_eligibility_check(
        self,
        student_id: int,
        eligible_scholarships: List[EligibilityScholar],
        student_data: Dict,
    ) -> EligibilityCheck:
        """Save an eligibility check result"""
        check = EligibilityCheck(
            student_id=student_id,
            eligible_scholarships=[s.model_dump() for s in eligible_scholarships],
            check_data=student_data,
            result_summary=f"Found {len(eligible_scholarships)} eligible scholarships",
        )
        self.db.add(check)
        self.db.commit()
        self.db.refresh(check)
        return check
