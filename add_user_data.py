import os
import sys

# Ensure app is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.services.rag_service import rag_service

raw_text = """
📝 SC | SCA | ST | SCC Scholarships
Eligible Criteria:
Government Quota & Management Quota (7.5 Category Not Eligible)
Annual Family Income Below 2.5Lakhs
Bank Seeding Active with Individual Bank Account

Required Documents :
Community Certificate
Income Certificate
Allotment Order (Government Quota Counselling Students Only)
Aadhaar Xerox
Aadhar Linked Mobile Number & Phone

📝 BC | MBC | DNC Scholarships
Eligible Criteria:
Government Quota Only (7.5 Category & Management Quota Students Not Eligible)
Annual Family Income Below 2.5Lakhs
Bank Seeding Active with Individual Bank Account

Required Documents :
Community Certificate
Income Certificate
First Graduation Certificate
Provisional Allotment Order (DoTE) 
Aadhaar Xerox
Aadhar Linked Mobile Number & Phone

📝 Pudhumai Penn & Tamil Puthalvan Scheme
Eligible Criteria:
6th to 12th Government School (Tamil & English Medium)
6th to 12th Government Fully Aided School (Tamil Medium Only)
Bank Seeding Active with Individual Bank Account

Required Documents :
10th & 12th Marksheet & TC
Aadhar Linked Mobile Number & Phone

📝 National Scholarship Portal
📌 1. AICTE – Swanath Scholarship Scheme (For Technical Diploma and Technical Degree)
Eligibility:
Orphan students who lost one or both parents due to COVID-19
Wards of Armed Forces/Central Paramilitary Forces martyred in action
Annual family income ≤ ₹8,00,000
Must be enrolled in AICTE-approved regular diploma/degree programs

📌 2. AICTE – Saksham Scholarship Scheme (For Specially Abled Students – Technical Degree/Diploma)
Eligibility:
Open to students with ≥ 40% disability
Annual family income ≤ ₹8,00,000
Admitted to first year of AICTE-approved technical degree/diploma course

📌 3. AICTE – Pragati Scholarship Scheme (For Girl Students – Technical Degree/Diploma)
Eligibility:
Admitted in 1st year or 2nd year (lateral entry) of AICTE-approved institution
Maximum 2 girl students per family can apply
Annual family income ≤ ₹8,00,000
For married applicants, higher income of parents or in-laws will be considered

📌 4. PM-USP Special Scholarship Scheme (For Students from Jammu & Kashmir and Ladakh)
Eligibility:
Domicile of Jammu & Kashmir or Ladakh
Passed Class 12 from JKBOSE or CBSE in 2021–22 or 2022–23
Diploma holders from UT polytechnics eligible for 2nd-year admission
Annual family income < ₹8,00,000

📌 5. AICTE – GATE/CEED Scholarship
Eligibility:
Must have a valid GATE/CEED 2025 score at the time of admission
Only for students in full-time AICTE-approved PG programs
Not eligible: Foreign students, sponsored/management quota, or part-time students
Must have an Aadhar-linked savings bank account (not joint or Jan-Dhan)
Must upload valid SC/ST/OBC (NCL)/PH certificates if applicable
Scholarship is available for up to 24 months or until course completion/thesis submission

📝 Management Scholarships
Please wait 📀... 

📝 Private Scholarships
Aspire - Harihara Subramanian Scholarship
Eligibility Criteria
Students must have scored 70% or above in both 10th and 12th standard examinations.
Open to First-Year students from the following streams:
CSE / IT / ECE / EEE / VLSI / AI & DS / AIML.
Both Counselling and Management quota students are eligible to apply.
Annual family income should be ₹3.0 lakhs or below.
Application Link : https://pearltrifoundation.org/form/ 

Reliance Foundation Undergraduate Scholarship 
Eligibility Criteria
1. Be a resident citizen of India 
2. Students who have passed std. 12th with a minimum of 60% marks and enrolled in 1st year regular full-time UG degree in any stream. 
3. Students having House Hold income < Rs. 15 lacs (preference given to <Rs.2.5 lacs)
Application Link : Undergraduate Scholarship Details & Application

Reliance Foundation Postgraduate Scholarships 
Eligibility Criteria
Resident of India 
First year regular full time PG Students with a score of 550 - 1,000 in the GATE Examination. 
Students who have scored 7.5 or above in their Undergraduate CGPA (or % normalised to CGPA) 
Eligible degree programmes – Select future-ready courses in Engineering, Technology, Energy and Life-Sciences. Please refer to the website for the full list of eligible programmes.
Application Link : Postgraduate Scholarship Details & Application 

Infosys Foundation STEM Stars Scholarship Program
Eligibility Criteria
Candidates must be Indian female students.
Candidates must have completed Class 12.
Students must be enrolled in first-year undergraduate courses at reputable (NIRF-accredited) institutions in STEM-related courses. Also, students pursuing second-year B.Arch or five-year Integrated/Dual Degree courses are eligible to apply.
Applicants must have an annual family income of less than or equal to ₹ 8,00,000.
Application Link : https://www.buddy4study.com/page/infosys-stem-stars-scholarship  
"""


def chunk_data():
    documents = []
    blocks = raw_text.split("📝 ")
    for block in blocks:
        if not block.strip():
            continue

        lines = block.strip().split("\n")
        title = lines[0].strip()

        if "National Scholarship Portal" in title:
            # Sub chunk NSP
            nsp_chunks = block.split("📌 ")
            for sub in nsp_chunks[1:]:  # skip first which is just the header
                sub_lines = sub.strip().split("\n")
                sub_title = sub_lines[0].strip()
                content = sub.strip()
                documents.append(
                    {
                        "content": "Category: National Scholarship Portal\nScholarship: "
                        + sub_title
                        + "\n"
                        + content,
                        "source": "Provided Texts",
                        "scholarship_name": sub_title,
                        "doc_type": "scholarship_info",
                    }
                )
        elif "Private Scholarships" in title:
            # Sub chunk Private
            priv_chunks = block.split("\n\n")
            for chunk in priv_chunks[1:]:
                if len(chunk.strip()) > 10:
                    priv_lines = chunk.strip().split("\n")
                    sub_title = priv_lines[0].strip()
                    documents.append(
                        {
                            "content": "Category: Private Scholarships\nScholarship: "
                            + sub_title
                            + "\n"
                            + chunk.strip(),
                            "source": "Provided Texts",
                            "scholarship_name": sub_title,
                            "doc_type": "scholarship_info",
                        }
                    )
        elif "Management Scholarships" in title:
            pass  # ignore waiting
        else:
            documents.append(
                {
                    "content": "Scholarship Category: " + title + "\n" + block.strip(),
                    "source": "Provided Texts",
                    "scholarship_name": title,
                    "doc_type": "scholarship_info",
                }
            )

    print(f"Generated {len(documents)} chunks.")
    rag_service.add_documents(documents)
    print("Added to FAISS DB!")


if __name__ == "__main__":
    chunk_data()
