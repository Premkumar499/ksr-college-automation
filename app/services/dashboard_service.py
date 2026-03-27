from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import Scholarship, Student, ScholarshipRecipient, ScholarshipApplication
from app.schemas.scholarship import DashboardResponse, DashboardStats, ScholarshipStats, RecipientInfo

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_data(self) -> DashboardResponse:
        """Get all dashboard statistics and data"""
        
        # Get overall stats
        stats = self._get_stats()
        
        # Get scholarship breakdown
        scholarship_breakdown = self._get_scholarship_stats()
        
        # Get recent recipients
        recent_recipients = self._get_recent_recipients(limit=10)
        
        return DashboardResponse(
            stats=stats,
            scholarship_breakdown=scholarship_breakdown,
            recent_recipients=recent_recipients
        )
    
    def _get_stats(self) -> DashboardStats:
        """Calculate overall statistics"""
        total_scholarships = self.db.query(Scholarship).filter(
            Scholarship.is_active == True
        ).count()
        
        total_eligible_students = self.db.query(Student).count()
        
        total_applications = self.db.query(ScholarshipApplication).count()
        
        total_disbursed = self.db.query(func.sum(ScholarshipRecipient.amount_disbursed)).scalar() or 0.0
        
        return DashboardStats(
            total_scholarships=total_scholarships,
            total_eligible_students=total_eligible_students,
            total_applications=total_applications,
            total_disbursed_amount=float(total_disbursed)
        )
    
    def _get_scholarship_stats(self) -> List[ScholarshipStats]:
        """Get statistics for each scholarship"""
        scholarships = self.db.query(Scholarship).all()
        stats = []
        
        for scholarship in scholarships:
            recipients = self.db.query(ScholarshipRecipient).filter(
                ScholarshipRecipient.scholarship_id == scholarship.id
            ).all()
            
            total_amount = sum(r.amount_disbursed for r in recipients)
            
            # Calculate average GPA of recipients
            avg_gpa = None
            if recipients:
                student_ids = [r.student_id for r in recipients]
                students = self.db.query(Student).filter(Student.id.in_(student_ids)).all()
                gpas = [s.gpa for s in students if s.gpa]
                if gpas:
                    avg_gpa = sum(gpas) / len(gpas)
            
            stats.append(ScholarshipStats(
                scholarship_id=scholarship.id,
                scholarship_name=scholarship.name,
                total_recipients=len(recipients),
                total_amount_disbursed=total_amount,
                average_gpa=round(avg_gpa, 2) if avg_gpa else None
            ))
        
        return stats
    
    def _get_recent_recipients(self, limit: int = 10) -> List[RecipientInfo]:
        """Get recent scholarship recipients"""
        recipients = self.db.query(ScholarshipRecipient).order_by(
            ScholarshipRecipient.disbursed_at.desc()
        ).limit(limit).all()
        
        result = []
        for r in recipients:
            student = self.db.query(Student).filter(Student.id == r.student_id).first()
            scholarship = self.db.query(Scholarship).filter(Scholarship.id == r.scholarship_id).first()
            
            if student and scholarship:
                result.append(RecipientInfo(
                    student_id=student.student_id,
                    student_name=student.name,
                    department=student.department or "N/A",
                    scholarship_name=scholarship.name,
                    amount=r.amount_disbursed,
                    academic_year=r.academic_year or "N/A"
                ))
        
        return result
    
    def get_scholarship_recipients(self, scholarship_id: int) -> List[RecipientInfo]:
        """Get all recipients for a specific scholarship"""
        recipients = self.db.query(ScholarshipRecipient).filter(
            ScholarshipRecipient.scholarship_id == scholarship_id
        ).all()
        
        result = []
        for r in recipients:
            student = self.db.query(Student).filter(Student.id == r.student_id).first()
            scholarship = self.db.query(Scholarship).filter(Scholarship.id == r.scholarship_id).first()
            
            if student and scholarship:
                result.append(RecipientInfo(
                    student_id=student.student_id,
                    student_name=student.name,
                    department=student.department or "N/A",
                    scholarship_name=scholarship.name,
                    amount=r.amount_disbursed,
                    academic_year=r.academic_year or "N/A"
                ))
        
        return result
