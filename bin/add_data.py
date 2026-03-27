import requests
import json

API_URL = "http://127.0.0.1:8000/scholarships/"

scholarships = [
    {
        "name": "SC | SCA | ST | SCC Scholarships",
        "provider": "Government of Tamil Nadu",
        "description": "Scholarship for SC, SCA, ST, and SCC category students.",
        "eligibility_criteria": {
            "category": ["SC", "SCA", "ST", "SCC"],
            "max_income": 250000
        },
        "documents_required": [
            "Community Certificate",
            "Income Certificate",
            "Allotment Order (Government Quota Counselling Students Only)",
            "Aadhaar Xerox",
            "Aadhar Linked Mobile Number & Phone"
        ],
        "application_procedure": "Bank Seeding Active with Individual Bank Account"
    },
    {
        "name": "BC | MBC | DNC Scholarships",
        "provider": "Government of Tamil Nadu",
        "description": "Scholarship for BC, MBC, and DNC category students admitted via Government Quota.",
        "eligibility_criteria": {
            "category": ["BC", "MBC", "DNC"],
            "max_income": 250000
        },
        "documents_required": [
            "Community Certificate",
            "Income Certificate",
            "First Graduation Certificate",
            "Provisional Allotment Order (DoTE)",
            "Aadhaar Xerox",
            "Aadhar Linked Mobile Number & Phone"
        ],
        "application_procedure": "Bank Seeding Active with Individual Bank Account"
    },
    {
        "name": "Pudhumai Penn & Tamil Puthalvan Scheme",
        "provider": "Government of Tamil Nadu",
        "description": "For students from 6th to 12th Government School (Tamil & English Medium) or Fully Aided School (Tamil Medium Only).",
        "eligibility_criteria": {
            "school_type": "Government or Fully Aided from 6th to 12th"
        },
        "documents_required": [
            "10th & 12th Marksheet & TC",
            "Aadhar Linked Mobile Number & Phone"
        ],
        "application_procedure": "Bank Seeding Active with Individual Bank Account"
    },
    {
        "name": "AICTE – Swanath Scholarship Scheme",
        "provider": "National Scholarship Portal",
        "description": "For Technical Diploma and Technical Degree. Orphan students who lost one/both parents due to COVID-19 or Wards of Armed Forces martyred in action.",
        "eligibility_criteria": {
            "max_income": 800000
        },
        "documents_required": [],
        "application_procedure": "Register on NSP OTR: https://scholarships.gov.in/"
    },
    {
        "name": "AICTE – Saksham Scholarship Scheme",
        "provider": "National Scholarship Portal",
        "description": "For Specially Abled Students (>= 40% disability) pursuing Technical Degree/Diploma.",
        "eligibility_criteria": {
            "max_income": 800000,
            "eligible_years": [1]
        },
        "documents_required": [],
        "application_procedure": "Register on NSP OTR: https://scholarships.gov.in/"
    },
    {
        "name": "AICTE – Pragati Scholarship Scheme",
        "provider": "National Scholarship Portal",
        "description": "For Girl Students pursuing Technical Degree/Diploma.",
        "eligibility_criteria": {
            "max_income": 800000,
            "gender": ["Female"],
            "eligible_years": [1, 2]
        },
        "documents_required": [],
        "application_procedure": "Register on NSP OTR: https://scholarships.gov.in/"
    },
    {
        "name": "PM-USP Special Scholarship Scheme",
        "provider": "National Scholarship Portal",
        "description": "For Students from Jammu & Kashmir and Ladakh.",
        "eligibility_criteria": {
            "max_income": 800000,
            "domicile": ["Jammu & Kashmir", "Ladakh"]
        },
        "documents_required": [],
        "application_procedure": "Register on NSP OTR: https://scholarships.gov.in/"
    },
    {
        "name": "AICTE – GATE/CEED Scholarship",
        "provider": "National Scholarship Portal",
        "description": "For students in full-time AICTE-approved PG programs with valid GATE/CEED 2025 score.",
        "eligibility_criteria": {
            "requires_gate": True
        },
        "documents_required": [
            "valid SC/ST/OBC (NCL)/PH certificates if applicable"
        ],
        "application_procedure": "Register on NSP OTR: https://scholarships.gov.in/. Must have an Aadhar-linked savings bank account."
    },
    {
        "name": "Aspire - Harihara Subramanian Scholarship",
        "provider": "Private - Pearl Tri Foundation",
        "description": "Open to First-Year students from CSE / IT / ECE / EEE / VLSI / AI & DS / AIML.",
        "eligibility_criteria": {
            "max_income": 300000,
            "min_gpa": 7.0,
            "eligible_years": [1],
            "department": ["CSE", "IT", "ECE", "EEE", "VLSI", "AI & DS", "AIML"]
        },
        "documents_required": [],
        "application_procedure": "Apply via link: https://pearltrifoundation.org/form/"
    },
    {
        "name": "Reliance Foundation Undergraduate Scholarship",
        "provider": "Private",
        "description": "For 1st year regular full-time UG degree students in any stream.",
        "eligibility_criteria": {
            "max_income": 1500000,
            "min_gpa": 6.0,
            "eligible_years": [1]
        },
        "documents_required": [],
        "application_procedure": "Undergraduate Scholarship Details & Application on Reliance Foundation site."
    },
    {
        "name": "Reliance Foundation Postgraduate Scholarships",
        "provider": "Private",
        "description": "For first year regular full time PG Students in Engineering, Technology, Energy and Life-Sciences.",
        "eligibility_criteria": {
            "min_gpa": 7.5,
            "eligible_years": [1],
            "requires_gate": True
        },
        "documents_required": [],
        "application_procedure": "Postgraduate Scholarship Details & Application on Reliance Foundation site."
    },
    {
        "name": "Infosys Foundation STEM Stars Scholarship Program",
        "provider": "Private",
        "description": "For Indian female students in first-year undergraduate STEM-related courses at NIRF-accredited institutions.",
        "eligibility_criteria": {
            "max_income": 800000,
            "gender": ["Female"],
            "eligible_years": [1, 2]
        },
        "documents_required": [],
        "application_procedure": "Apply via link: https://www.buddy4study.com/page/infosys-stem-stars-scholarship"
    }
]

def add_scholarships():
    success_count = 0
    for idx, scholarship in enumerate(scholarships):
        # We try to post to the API. If the API is running, it will add the data.
        try:
            response = requests.post(API_URL, json=scholarship)
            # 2xx indicates success
            if response.status_code >= 200 and response.status_code < 300:
                print(f"[{idx+1}/{len(scholarships)}] Successfully added: {scholarship['name']}")
                success_count += 1
            else:
                print(f"[{idx+1}/{len(scholarships)}] Failed to add: {scholarship['name']}. Status: {response.status_code}, Error: {response.text}")
        except Exception as e:
            print(f"[{idx+1}/{len(scholarships)}] Exception occurred while adding {scholarship['name']}: {e}")
            
    print(f"\nCompleted! Successfully added {success_count} out of {len(scholarships)} scholarships.")

if __name__ == '__main__':
    add_scholarships()
