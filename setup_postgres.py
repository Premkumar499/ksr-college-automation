"""
PostgreSQL Database Setup Script
Run this script to create the database and tables in PostgreSQL
"""

import psycopg2
from psycopg2 import sql
import psycopg2.extras
import os

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "office")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")


def create_database():
    """Create the scholarship_db database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
            )
            print(f"✓ Database '{DB_NAME}' created successfully!")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")
        raise


def create_tables():
    """Create all tables in the database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()

        # Create scholarships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scholarships (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                provider VARCHAR(255),
                description TEXT,
                eligibility_criteria JSONB,
                documents_required JSONB,
                application_procedure TEXT,
                deadline TIMESTAMP,
                amount FLOAT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'scholarships' created!")

        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20),
                department VARCHAR(100),
                year INTEGER,
                gpa FLOAT,
                category VARCHAR(50),
                family_income FLOAT,
                gender VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'students' created!")

        # Create eligibility_checks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eligibility_checks (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id),
                scholarship_id INTEGER REFERENCES scholarships(id),
                eligible_scholarships JSONB,
                check_data JSONB,
                result_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'eligibility_checks' created!")

        # Create scholarship_applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scholarship_applications (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id),
                scholarship_id INTEGER REFERENCES scholarships(id),
                status VARCHAR(50) DEFAULT 'pending',
                documents_submitted JSONB,
                notes TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'scholarship_applications' created!")

        # Create scholarship_recipients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scholarship_recipients (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id),
                scholarship_id INTEGER REFERENCES scholarships(id),
                academic_year VARCHAR(20),
                amount_disbursed FLOAT,
                status VARCHAR(50) DEFAULT 'disbursed',
                disbursed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'scholarship_recipients' created!")

        # Create chat_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id),
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                context_used JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'chat_history' created!")

        # Create indexes
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_student_id ON students(student_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_scholarship_active ON scholarships(is_active)"
        )
        print("✓ Indexes created!")

        conn.commit()
        cursor.close()
        conn.close()

        print("\n✅ PostgreSQL database setup complete!")

    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


def seed_scholarships():
    """Insert initial scholarship data"""
    scholarships = [
        {
            "name": "SC | SCA | ST | SCC Scholarships",
            "provider": "Government of Tamil Nadu",
            "description": "Scholarship for SC, SCA, ST, and SCC category students.",
            "eligibility_criteria": {
                "category": ["SC", "SCA", "ST", "SCC"],
                "max_income": 250000,
            },
            "documents_required": [
                "Community Certificate",
                "Income Certificate",
                "Allotment Order",
                "Aadhaar Xerox",
                "Aadhar Linked Mobile Number",
            ],
            "application_procedure": "Apply through Tamil Nadu scholarship portal",
        },
        {
            "name": "BC | MBC | DNC Scholarships",
            "provider": "Government of Tamil Nadu",
            "description": "Scholarship for BC, MBC, and DNC category students.",
            "eligibility_criteria": {
                "category": ["BC", "MBC", "DNC"],
                "max_income": 250000,
            },
            "documents_required": [
                "Community Certificate",
                "Income Certificate",
                "First Graduation Certificate",
                "Provisional Allotment Order",
            ],
            "application_procedure": "Apply through Tamil Nadu scholarship portal",
        },
        {
            "name": "Pudhumai Penn & Tamil Puthalvan Scheme",
            "provider": "Government of Tamil Nadu",
            "description": "For students from 6th to 12th Government School.",
            "eligibility_criteria": {"school_type": "Government or Fully Aided"},
            "documents_required": [
                "10th & 12th Marksheet & TC",
                "Aadhar Linked Mobile Number",
            ],
            "application_procedure": "Apply through Tamil Nadu scholarship portal",
        },
        {
            "name": "AICTE – Swanath Scholarship",
            "provider": "National Scholarship Portal",
            "description": "For orphan students or wards of armed forces martyred in action.",
            "eligibility_criteria": {"max_income": 800000, "min_gpa": 6.0},
            "documents_required": [],
            "application_procedure": "Register on NSP: https://scholarships.gov.in/",
        },
        {
            "name": "AICTE – Saksham Scholarship",
            "provider": "National Scholarship Portal",
            "description": "For Specially Abled Students (>= 40% disability).",
            "eligibility_criteria": {"max_income": 800000, "eligible_years": [1]},
            "documents_required": ["Disability Certificate"],
            "application_procedure": "Register on NSP: https://scholarships.gov.in/",
        },
        {
            "name": "AICTE – Pragati Scholarship",
            "provider": "National Scholarship Portal",
            "description": "For Girl Students pursuing Technical Degree/Diploma.",
            "eligibility_criteria": {
                "max_income": 800000,
                "gender": ["Female"],
                "eligible_years": [1, 2],
            },
            "documents_required": [],
            "application_procedure": "Register on NSP: https://scholarships.gov.in/",
        },
        {
            "name": "PM-USP Special Scholarship",
            "provider": "National Scholarship Portal",
            "description": "For Students from Jammu & Kashmir and Ladakh.",
            "eligibility_criteria": {
                "max_income": 800000,
                "domicile": ["Jammu & Kashmir", "Ladakh"],
            },
            "documents_required": [],
            "application_procedure": "Register on NSP: https://scholarships.gov.in/",
        },
        {
            "name": "AICTE – GATE/CEED Scholarship",
            "provider": "National Scholarship Portal",
            "description": "For students with valid GATE/CEED score in PG programs.",
            "eligibility_criteria": {"requires_gate": True},
            "documents_required": ["GATE Score Card"],
            "application_procedure": "Register on NSP: https://scholarships.gov.in/",
        },
        {
            "name": "Aspire - Harihara Subramanian Scholarship",
            "provider": "Pearl Tri Foundation",
            "description": "For First-Year students from CSE/IT/ECE/EEE with 70%+ in 10th & 12th.",
            "eligibility_criteria": {
                "max_income": 300000,
                "min_gpa": 7.0,
                "eligible_years": [1],
                "department": ["CSE", "IT", "ECE", "EEE", "VLSI", "AI & DS", "AIML"],
            },
            "documents_required": ["10th & 12th Marksheets", "Income Certificate"],
            "application_procedure": "Apply: https://pearltrifoundation.org/form/",
        },
        {
            "name": "Reliance Foundation Undergraduate Scholarship",
            "provider": "Reliance Foundation",
            "description": "For 1st year UG students with 60%+ in 12th.",
            "eligibility_criteria": {
                "max_income": 1500000,
                "min_gpa": 6.0,
                "eligible_years": [1],
            },
            "documents_required": [],
            "application_procedure": "Apply on Reliance Foundation site",
        },
        {
            "name": "Reliance Foundation Postgraduate Scholarship",
            "provider": "Reliance Foundation",
            "description": "For PG students in Engineering, Technology, Energy, Life-Sciences.",
            "eligibility_criteria": {
                "min_gpa": 7.5,
                "eligible_years": [1],
                "requires_gate": True,
            },
            "documents_required": ["GATE Score Card", "Undergraduate Marksheet"],
            "application_procedure": "Apply on Reliance Foundation site",
        },
        {
            "name": "Infosys Foundation STEM Stars Scholarship",
            "provider": "Infosys Foundation",
            "description": "For Indian female students in STEM courses at NIRF institutions.",
            "eligibility_criteria": {
                "max_income": 800000,
                "gender": ["Female"],
                "eligible_years": [1, 2],
            },
            "documents_required": [],
            "application_procedure": "Apply: https://www.buddy4study.com/page/infosys-stem-stars-scholarship",
        },
    ]

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()

        for scholarship in scholarships:
            cursor.execute(
                """
                INSERT INTO scholarships (name, provider, description, eligibility_criteria, documents_required, application_procedure)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """,
                (
                    scholarship["name"],
                    scholarship["provider"],
                    scholarship["description"],
                    psycopg2.extras.Json(scholarship["eligibility_criteria"]),
                    psycopg2.extras.Json(scholarship["documents_required"]),
                    scholarship["application_procedure"],
                ),
            )

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✓ Seeded {len(scholarships)} scholarships!")

    except Exception as e:
        print(f"Error seeding scholarships: {e}")


if __name__ == "__main__":
    print("Setting up PostgreSQL database...\n")
    create_database()
    create_tables()
    seed_scholarships()
    print("\n📊 Connect to pgAdmin to view data!")
    print(f"   Host: {DB_HOST}")
    print(f"   Port: {DB_PORT}")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print(f"   Password: {DB_PASSWORD}")
