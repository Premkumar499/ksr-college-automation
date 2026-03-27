"""
Setup Script - Initialize the database and load sample data
"""

from app.core.database import engine, Base, SessionLocal
from app.models.database import Scholarship, Student, ScholarshipRecipient
from app.utils.data_loader import create_sample_scholarships
from datetime import datetime

def init_database():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def load_sample_data():
    """Load sample scholarship data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing = db.query(Scholarship).first()
        if existing:
            print("Sample data already exists. Skipping...")
            return
        
        # Load sample scholarships
        scholarships = create_sample_scholarships()
        for data in scholarships:
            scholarship = Scholarship(
                name=data['name'],
                provider=data['provider'],
                description=data['description'],
                eligibility_criteria=data['eligibility_criteria'],
                documents_required=data['documents_required'],
                application_procedure=data['application_procedure'],
                amount=data['amount'],
                deadline=datetime.fromisoformat(data['deadline']) if data['deadline'] else None
            )
            db.add(scholarship)
        
        db.commit()
        print(f"Loaded {len(scholarships)} sample scholarships!")
        
        # Add sample students
        sample_students = [
            Student(
                student_id="2021CS001",
                name="Rahul Kumar",
                email="rahul.kumar@college.edu",
                phone="9876543210",
                department="Computer Science",
                year=3,
                gpa=8.7,
                category="General",
                family_income=350000,
                gender="Male"
            ),
            Student(
                student_id="2022EC002",
                name="Priya Sharma",
                email="priya.sharma@college.edu",
                phone="9876543211",
                department="Electronics",
                year=2,
                gpa=9.2,
                category="OBC",
                family_income=180000,
                gender="Female"
            ),
            Student(
                student_id="2020ME003",
                name="Amit Singh",
                email="amit.singh@college.edu",
                phone="9876543212",
                department="Mechanical",
                year=4,
                gpa=7.5,
                category="SC",
                family_income=120000,
                gender="Male"
            )
        ]
        
        for student in sample_students:
            db.add(student)
        
        db.commit()
        print(f"Added {len(sample_students)} sample students!")
        
        # Add sample recipients
        scholarships = db.query(Scholarship).all()
        students = db.query(Student).all()
        
        if scholarships and students:
            recipients = [
                ScholarshipRecipient(
                    student_id=students[0].id,
                    scholarship_id=scholarships[0].id,
                    academic_year="2024-2025",
                    amount_disbursed=50000,
                    status="disbursed"
                ),
                ScholarshipRecipient(
                    student_id=students[1].id,
                    scholarship_id=scholarships[1].id,
                    academic_year="2024-2025",
                    amount_disbursed=25000,
                    status="disbursed"
                ),
                ScholarshipRecipient(
                    student_id=students[2].id,
                    scholarship_id=scholarships[2].id,
                    academic_year="2024-2025",
                    amount_disbursed=30000,
                    status="disbursed"
                )
            ]
            
            for r in recipients:
                db.add(r)
            
            db.commit()
            print(f"Added {len(recipients)} sample recipients!")
        
        print("\nSample data loaded successfully!")
        
    except Exception as e:
        print(f"Error loading sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Scholarship AI - Database Setup")
    print("=" * 50)
    print()
    
    init_database()
    load_sample_data()
    
    print()
    print("Setup complete!")
    print("\nNext steps:")
    print("1. Set up PostgreSQL database")
    print("2. Update .env file with your settings")
    print("3. Run the normal server: python -m app.main")
    print("4. Run the heavy server: python heavy_server/main.py")
    print("5. Open frontend/index.html in browser")
