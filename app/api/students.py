from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.database import Student
from app.schemas.scholarship import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    """Get all students"""
    students = db.query(Student).all()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a specific student by ID"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/by-college-id/{college_id}", response_model=StudentResponse)
def get_student_by_college_id(college_id: str, db: Session = Depends(get_db)):
    """Get a student by their college ID"""
    student = db.query(Student).filter(Student.student_id == college_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Register a new student"""
    existing = (
        db.query(Student)
        .filter(
            (Student.student_id == student.student_id)
            | (Student.email == student.email)
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Student already exists")

    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student: StudentCreate, db: Session = Depends(get_db)
):
    """Update student details"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student.model_dump().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student
