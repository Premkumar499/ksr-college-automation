from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import (
    Scholarship,
    Student,
    ScholarshipRecipient,
    ScholarshipApplication,
)
from app.schemas.scholarship import (
    DashboardResponse,
    DashboardStats,
    ScholarshipStats,
    RecipientInfo,
)


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_data(self) -> DashboardResponse:
        """Get all dashboard statistics and data"""

        # Get overall stats
        stats = self._get_stats()

        # Get scholarship breakdown
        scholarship_breakdown = self._get_scholarship_stats()

        # Get all recipients
        recent_recipients = self._get_recent_recipients()

        return DashboardResponse(
            stats=stats,
            scholarship_breakdown=scholarship_breakdown,
            recent_recipients=recent_recipients,
        )

    def _get_stats(self) -> DashboardStats:
        """Calculate overall statistics"""
        total_scholarships = (
            self.db.query(Scholarship).count()
        )

        total_eligible_students = self.db.query(Student).count()

        total_applications = 0

        total_disbursed = (
            self.db.query(func.sum(Student.scholarship_amount)).scalar()
            or 0.0
        )

        return DashboardStats(
            total_scholarships=total_scholarships,
            total_eligible_students=total_eligible_students,
            total_applications=total_applications,
            total_disbursed_amount=float(total_disbursed),
        )

    def _get_scholarship_stats(self) -> List[ScholarshipStats]:
        """Get statistics for each scholarship. Return empty list since the UI section is removed."""
        return []

    def _get_recent_recipients(self) -> List[RecipientInfo]:
        """Get all scholarship recipients directly from students table"""
        students = (
            self.db.query(Student)
            .all()
        )

        result = []
        for s in students:
            result.append(
                RecipientInfo(
                    student_id=str(s.student_id),
                    student_name=s.name or "Unknown",
                    department=s.department or "N/A",
                    scholarship_name=s.scheme_name or "N/A",
                    amount=float(s.scholarship_amount or 0.0),
                    academic_year=str(s.year) if s.year else "N/A",
                )
            )

        return result

    def get_scholarship_recipients(self, scholarship_id: int) -> List[RecipientInfo]:
        """Get all recipients for a specific scholarship (deprecated/fallback)"""
        return []
