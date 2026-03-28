"""
Data Loading Utilities - Load scholarship data from PDFs and Excel/CSV files
"""

import pandas as pd
from typing import List, Dict
from datetime import datetime


def load_scholarships_from_excel(file_path: str) -> List[Dict]:
    """Load scholarship data from Excel file"""
    df = pd.read_excel(file_path)
    scholarships = []

    for _, row in df.iterrows():
        scholarship = {
            "name": row.get("name", row.get("scholarship_name", "Unknown")),
            "provider": row.get("provider", row.get("offered_by", None)),
            "description": row.get("description", row.get("about", None)),
            "eligibility_criteria": parse_eligibility(row),
            "documents_required": parse_documents(row),
            "application_procedure": row.get(
                "procedure", row.get("how_to_apply", None)
            ),
            "amount": float(row["amount"]) if pd.notna(row.get("amount")) else None,
            "deadline": row.get("deadline", None),
        }
        scholarships.append(scholarship)

    return scholarships


def parse_eligibility(row: pd.Series) -> Dict:
    """Parse eligibility criteria from DataFrame row"""
    criteria = {}

    if pd.notna(row.get("min_gpa")):
        criteria["min_gpa"] = float(row["min_gpa"])

    if pd.notna(row.get("category")):
        categories = str(row["category"]).split(",")
        criteria["category"] = [c.strip() for c in categories]

    if pd.notna(row.get("max_income")):
        criteria["max_income"] = float(row["max_income"])

    if pd.notna(row.get("eligible_years")):
        years = str(row["eligible_years"]).split(",")
        criteria["eligible_years"] = [int(y.strip()) for y in years]

    if pd.notna(row.get("department")):
        criteria["department"] = str(row["department"]).split(",")

    return criteria


def parse_documents(row: pd.Series) -> List[str]:
    """Parse required documents from DataFrame row"""
    docs = row.get("documents_required", row.get("required_documents", ""))

    if pd.isna(docs):
        return []

    if isinstance(docs, str):
        return [d.strip() for d in docs.split(",")]

    return docs


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file"""
    import pdfplumber

    text_content = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)

    return "\n\n".join(text_content)


def create_sample_scholarships() -> List[Dict]:
    """Create sample scholarship data for testing"""
    return [
        {
            "name": "National Merit Scholarship",
            "provider": "Government of India",
            "description": "Scholarship for meritorious students from economically weaker sections",
            "eligibility_criteria": {
                "min_gpa": 8.5,
                "category": ["General", "OBC", "SC", "ST"],
                "max_income": 250000,
                "eligible_years": [2, 3, 4],
            },
            "documents_required": [
                "Income Certificate",
                "Caste Certificate (if applicable)",
                "Previous Year Marksheet",
                "Bank Account Details",
                "Aadhar Card",
            ],
            "application_procedure": "Apply online through National Scholarship Portal (NSP)",
            "amount": 50000,
            "deadline": "2025-06-30",
        },
        {
            "name": "Merit-Cum-Means Scholarship",
            "provider": "College Trust",
            "description": "Scholarship for students with good academics and financial need",
            "eligibility_criteria": {
                "min_gpa": 7.5,
                "max_income": 400000,
                "category": ["General", "OBC", "SC", "ST"],
            },
            "documents_required": [
                "Income Certificate",
                "Previous Year Marksheet",
                "Fee Receipt",
                "Photograph",
                "Application Form",
            ],
            "application_procedure": "Submit application to College Scholarship Cell",
            "amount": 25000,
            "deadline": datetime(2025, 7, 15),
        },
        {
            "name": "SC/ST Post Matric Scholarship",
            "provider": "State Government",
            "description": "Post-matriculation scholarship for SC/ST students",
            "eligibility_criteria": {
                "min_gpa": 6.0,
                "category": ["SC", "ST"],
                "max_income": 250000,
            },
            "documents_required": [
                "Caste Certificate",
                "Income Certificate",
                "Previous Marksheet",
                "Domicile Certificate",
                "Bank Passbook Copy",
            ],
            "application_procedure": "Apply through State Scholarship Portal",
            "amount": 30000,
            "deadline": datetime(2025, 8, 1),
        },
    ]
