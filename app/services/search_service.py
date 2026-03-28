from typing import List, Dict


class SimpleSearchService:
    """Simple keyword-based search for scholarships"""

    def __init__(self):
        self.scholarships = self._load_scholarships()

    def _load_scholarships(self) -> List[Dict]:
        return [
            {
                "name": "SC | SCA | ST | SCC Scholarships",
                "source": "Government of Tamil Nadu",
                "category": "government",
                "keywords": [
                    "sc",
                    "st",
                    "scc",
                    "sca",
                    "scheduled caste",
                    "sc scholarship",
                    "st scholarship",
                ],
                "content": """**SC | SCA | ST | SCC Scholarships**
Government of Tamil Nadu

**Eligibility Criteria:**
• Government Quota & Management Quota (7.5 Category Not Eligible)
• Annual Family Income Below ₹2.5 Lakhs
• Bank Seeding Active with Individual Bank Account

**Required Documents:**
• Community Certificate
• Income Certificate
• Allotment Order (Government Quota Counselling Students Only)
• Aadhaar Xerox
• Aadhar Linked Mobile Number & Phone""",
            },
            {
                "name": "BC | MBC | DNC Scholarships",
                "source": "Government of Tamil Nadu",
                "category": "government",
                "keywords": [
                    "bc",
                    "mbc",
                    "dnc",
                    "backward class",
                    "bc scholarship",
                    "mbc scholarship",
                ],
                "content": """**BC | MBC | DNC Scholarships**
Government of Tamil Nadu

**Eligibility Criteria:**
• Government Quota Only (7.5 Category & Management Quota Students Not Eligible)
• Annual Family Income Below ₹2.5 Lakhs
• Bank Seeding Active with Individual Bank Account

**Required Documents:**
• Community Certificate
• Income Certificate
• First Graduation Certificate
• Provisional Allotment Order (DoTE)
• Aadhaar Xerox
• Aadhar Linked Mobile Number & Phone""",
            },
            {
                "name": "Pudhumai Penn & Tamil Puthalvan Scheme",
                "source": "Government of Tamil Nadu",
                "category": "government",
                "keywords": [
                    "pudhumai",
                    "pudhumaipp",
                    "tamil pudhalvan",
                    "pudhumai penn",
                ],
                "content": """**Pudhumai Penn & Tamil Puthalvan Scheme**
Government of Tamil Nadu

**Eligibility Criteria:**
• 6th to 12th Government School (Tamil & English Medium)
• 6th to 12th Government Fully Aided School (Tamil Medium Only)
• Bank Seeding Active with Individual Bank Account

**Required Documents:**
• 10th & 12th Marksheet & TC
• Aadhar Linked Mobile Number & Phone""",
            },
            {
                "name": "AICTE – Swanath Scholarship Scheme",
                "source": "National Scholarship Portal",
                "category": "aicte",
                "keywords": [
                    "swanath",
                    "aicte swanath",
                    "orphan",
                    "armed forces",
                    "covid",
                ],
                "content": """**AICTE – Swanath Scholarship Scheme**
National Scholarship Portal

**Eligibility:**
• Orphan students who lost one or both parents due to COVID-19
• Wards of Armed Forces/Central Paramilitary Forces martyred in action
• Annual family income ≤ ₹8,00,000
• Must be enrolled in AICTE-approved regular diploma/degree programs

**Required Documents:**
• Orphan Certificate (if applicable)
• Armed Forces Certificate (if applicable)
• Income Certificate
• College Admission Documents

**Apply at:** https://scholarships.gov.in/""",
            },
            {
                "name": "AICTE – Saksham Scholarship Scheme",
                "source": "National Scholarship Portal",
                "category": "aicte",
                "keywords": [
                    "saksham",
                    "aicte saksham",
                    "disability",
                    "specially abled",
                    "disabled",
                ],
                "content": """**AICTE – Saksham Scholarship Scheme**
National Scholarship Portal

**Eligibility:**
• Open to students with ≥40% disability
• Annual family income ≤ ₹8,00,000
• Admitted to first year of AICTE-approved technical degree/diploma course

**Required Documents:**
• Disability Certificate (≥40% disability)
• Income Certificate
• College Admission Documents

**Apply at:** https://scholarships.gov.in/""",
            },
            {
                "name": "AICTE – Pragati Scholarship Scheme",
                "source": "National Scholarship Portal",
                "category": "aicte",
                "keywords": ["pragati", "aicte pragati", "girl students", "female"],
                "content": """**AICTE – Pragati Scholarship Scheme**
National Scholarship Portal

**Eligibility:**
• Admitted in 1st year or 2nd year (lateral entry) of AICTE-approved institution
• Maximum 2 girl students per family can apply
• Annual family income ≤ ₹8,00,000

**Required Documents:**
• College Admission Documents
• Income Certificate
• Aadhaar Card
• Bank Account Details

**Apply at:** https://scholarships.gov.in/""",
            },
            {
                "name": "PM-USP Special Scholarship Scheme",
                "source": "National Scholarship Portal",
                "category": "aicte",
                "keywords": ["pm-usp", "pm usp", "jammu", "kashmir", "ladakh", "j&k"],
                "content": """**PM-USP Special Scholarship Scheme**
National Scholarship Portal

**Eligibility:**
• Domicile of Jammu & Kashmir or Ladakh
• Passed Class 12 from JKBOSE or CBSE in 2021–22 or 2022–23
• Diploma holders from UT polytechnics eligible for 2nd-year admission
• Annual family income < ₹8,00,000

**Required Documents:**
• Domicile Certificate (Jammu & Kashmir or Ladakh)
• Class 12 Marksheet
• Income Certificate
• College Admission Documents

**Apply at:** https://scholarships.gov.in/""",
            },
            {
                "name": "AICTE – GATE/CEED Scholarship",
                "source": "National Scholarship Portal",
                "category": "aicte",
                "keywords": ["gate", "ceed", "aicte gate", "postgraduate", "pg"],
                "content": """**AICTE – GATE/CEED Scholarship**
National Scholarship Portal

**Eligibility:**
• Must have a valid GATE/CEED 2025 score at the time of admission
• Only for students in full-time AICTE-approved PG programs
• Not eligible: Foreign students, sponsored/management quota, or part-time students
• Must have an Aadhar-linked savings bank account (not joint or Jan-Dhan)
• Available for up to 24 months or until course completion/thesis submission

**Required Documents:**
• GATE/CEED Score Card
• College Admission Documents
• Aadhaar-linked Bank Account

**Apply at:** https://scholarships.gov.in/""",
            },
            {
                "name": "Aspire - Harihara Subramanian Scholarship",
                "source": "Private - Pearl Tri Foundation",
                "category": "private",
                "keywords": ["aspire", "harihara", "pearl tri", "aspire scholarship"],
                "content": """**Aspire - Harihara Subramanian Scholarship**
Pearl Tri Foundation

**Eligibility:**
• 70% or above in both 10th and 12th standard examinations
• First-Year students from: CSE / IT / ECE / EEE / VLSI / AI & DS / AIML
• Both Counselling and Management quota students eligible
• Annual family income ≤ ₹3.0 lakhs

**Required Documents:**
• 10th & 12th Marksheets
• Income Certificate
• College Admission Documents

**Apply at:** https://pearltrifoundation.org/form/""",
            },
            {
                "name": "Reliance Foundation Undergraduate Scholarship",
                "source": "Private - Reliance Foundation",
                "category": "private",
                "keywords": [
                    "reliance",
                    "reliance foundation",
                    "reliance undergraduate",
                ],
                "content": """**Reliance Foundation Undergraduate Scholarship**

**Eligibility:**
• Resident citizen of India
• Passed std. 12th with minimum 60% marks
• Enrolled in 1st year regular full-time UG degree
• House Hold income < Rs. 15 lakhs (preference < Rs.2.5 lakhs)

**Required Documents:**
• 12th Marksheet
• Income Certificate
• College Admission Documents
• Aadhaar Card
• Bank Account Details

**Apply at:** Reliance Foundation site""",
            },
            {
                "name": "Reliance Foundation Postgraduate Scholarships",
                "source": "Private - Reliance Foundation",
                "category": "private",
                "keywords": ["reliance", "reliance postgraduate", "reliance pg"],
                "content": """**Reliance Foundation Postgraduate Scholarships**

**Eligibility:**
• Resident of India
• First year regular full time PG Students
• GATE score 550-1000 OR 7.5+ CGPA in Undergraduate
• Engineering, Technology, Energy and Life-Sciences

**Required Documents:**
• GATE Score Card (if applicable)
• Undergraduate Marksheet/CGPA Certificate
• Income Certificate
• College Admission Documents
• Aadhaar Card

**Apply at:** Reliance Foundation site""",
            },
            {
                "name": "Infosys Foundation STEM Stars Scholarship",
                "source": "Private - Infosys Foundation",
                "category": "private",
                "keywords": [
                    "infosys",
                    "stem stars",
                    "infosys scholarship",
                    "female students",
                ],
                "content": """**Infosys Foundation STEM Stars Scholarship Program**

**Eligibility:**
• Indian female students only
• Completed Class 12
• First-year undergraduate at NIRF-accredited STEM institutions
• Also eligible: second-year B.Arch or five-year Integrated/Dual Degree courses
• Annual family income ≤ ₹8,00,000

**Required Documents:**
• Class 12 Marksheet
• Income Certificate
• College Admission Documents (NIRF-accredited institution)
• Aadhaar Card
• Bank Account Details

**Apply at:** https://www.buddy4study.com/page/infosys-stem-stars-scholarship""",
            },
        ]

    def search(self, query: str, max_results: int = 1) -> List[Dict]:
        """Search for scholarships by keywords"""
        query_lower = query.lower()
        query_words = query_lower.split()

        import re
        results = []

        for scholarship in self.scholarships:
            score = 0

            for keyword in scholarship["keywords"]:
                if re.search(rf"\b{re.escape(keyword)}\b", query_lower):
                    score += 10
                # Give extra weight if the entire query exactly matches a keyword
                if keyword == query_lower.strip():
                    score += 50

            name_lower = scholarship["name"].lower()
            if name_lower.replace("–", "-").replace("  ", " ") in query_lower.replace(
                "–", "-"
            ):
                score += 20

            if score > 0:
                results.append(
                    {
                        "name": scholarship["name"],
                        "content": scholarship["content"],
                        "score": score,
                    }
                )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]

    def get_context(self, query: str) -> str:
        """Get formatted context for a query"""
        results = self.search(query, max_results=1)

        if not results:
            return ""

        return results[0]["content"]

    def get_all_names(self) -> List[str]:
        """Get list of all scholarship names"""
        return [s["name"] for s in self.scholarships]


search_service = SimpleSearchService()
