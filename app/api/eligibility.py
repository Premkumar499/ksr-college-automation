from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.scholarship import (
    EligibilityCheckRequest,
    EligibilityCheckResponse,
    StudentCreate,
)
from app.services.eligibility_service import EligibilityService
from app.models.database import Student

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])


def orm_to_dict(obj) -> dict:
    result = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        result[col.name] = val
    return result


@router.post("/check", response_model=EligibilityCheckResponse)
def check_eligibility(request: EligibilityCheckRequest, db: Session = Depends(get_db)):
    """
    Check which scholarships a student is eligible for.

    Provide either:
    - student_id: If the student is already registered
    - student_data: Full student details for a one-time check
    """
    eligibility_service = EligibilityService(db)

    if request.student_id:
        student = db.query(Student).filter(Student.id == request.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        student_dict = orm_to_dict(student)
        student_data = StudentCreate(
            student_id=str(student_dict.get("student_id", "")),
            name=str(student_dict.get("name", "")),
            email=str(student_dict.get("email", "")),
            phone=student_dict.get("phone"),
            department=student_dict.get("department"),
            year=student_dict.get("year"),
            gpa=student_dict.get("gpa"),
            category=student_dict.get("category"),
            family_income=student_dict.get("family_income"),
            gender=student_dict.get("gender"),
        )
    elif request.student_data:
        student_data = request.student_data
    else:
        raise HTTPException(
            status_code=400, detail="Either student_id or student_data must be provided"
        )

    eligible_scholarships = eligibility_service.check_eligibility(student_data)

    check_id = None
    if request.student_id:
        check = eligibility_service.save_eligibility_check(
            student_id=request.student_id,
            eligible_scholarships=eligible_scholarships,
            student_data=student_data.model_dump(),
        )
        check_id = check.id

    return EligibilityCheckResponse(
        eligible_scholarships=eligible_scholarships,
        total_found=len(eligible_scholarships),
        check_id=check_id,
    )


@router.get("/history/{student_id}")
def get_eligibility_history(student_id: int, db: Session = Depends(get_db)):
    """Get eligibility check history for a student"""
    from app.models.database import EligibilityCheck

    checks = (
        db.query(EligibilityCheck)
        .filter(EligibilityCheck.student_id == student_id)
        .order_by(EligibilityCheck.created_at.desc())
        .all()
    )

    return {"checks": checks}
