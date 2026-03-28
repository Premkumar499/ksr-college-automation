from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.database import Scholarship
from app.schemas.scholarship import ScholarshipCreate, ScholarshipResponse

router = APIRouter(prefix="/scholarships", tags=["Scholarships"])


@router.get("/", response_model=List[ScholarshipResponse])
def list_scholarships(db: Session = Depends(get_db)):
    """Get all active scholarships"""
    scholarships = db.query(Scholarship).filter(Scholarship.is_active).all()
    return scholarships


@router.get("/{scholarship_id}", response_model=ScholarshipResponse)
def get_scholarship(scholarship_id: int, db: Session = Depends(get_db)):
    """Get a specific scholarship by ID"""
    scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship


@router.post("/", response_model=ScholarshipResponse)
def create_scholarship(scholarship: ScholarshipCreate, db: Session = Depends(get_db)):
    """Create a new scholarship"""
    db_scholarship = Scholarship(**scholarship.model_dump())
    db.add(db_scholarship)
    db.commit()
    db.refresh(db_scholarship)
    return db_scholarship


@router.put("/{scholarship_id}", response_model=ScholarshipResponse)
def update_scholarship(
    scholarship_id: int, scholarship: ScholarshipCreate, db: Session = Depends(get_db)
):
    """Update an existing scholarship"""
    db_scholarship = (
        db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    )
    if not db_scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    for key, value in scholarship.model_dump().items():
        setattr(db_scholarship, key, value)

    db.commit()
    db.refresh(db_scholarship)
    return db_scholarship


@router.delete("/{scholarship_id}")
def delete_scholarship(scholarship_id: int, db: Session = Depends(get_db)):
    """Soft delete a scholarship"""
    db_scholarship = (
        db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    )
    if not db_scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    db_scholarship.is_active = bool(False)
    db.commit()
    return {"message": "Scholarship deleted successfully"}
