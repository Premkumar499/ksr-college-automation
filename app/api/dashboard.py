from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.scholarship import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    """
    Get dashboard statistics and data.
    
    Returns:
    - Overall statistics (total scholarships, students, applications, disbursed amount)
    - Scholarship-wise breakdown with recipient counts and amounts
    - Recent scholarship recipients
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_dashboard_data()

@router.get("/scholarship/{scholarship_id}/recipients")
def get_scholarship_recipients(scholarship_id: int, db: Session = Depends(get_db)):
    """Get all recipients for a specific scholarship"""
    dashboard_service = DashboardService(db)
    recipients = dashboard_service.get_scholarship_recipients(scholarship_id)
    return {"recipients": recipients}
