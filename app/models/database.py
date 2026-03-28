from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    scheme_name = Column(String(200), nullable=False)
    eligibility_criteria = Column(Text)
    application_link = Column(Text)
    category = Column(String(100))
    
    # We remove recipients relationship since scholarship_recipients schema might be broken too, 
    # but we will just keep the relationship to avoid breaking existing imports.
    recipients = relationship("ScholarshipRecipient", back_populates="scholarship")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), nullable=True, index=True)
    name = Column(String(100), nullable=True)
    scholarship_amount = Column(Float, nullable=True)
    scheme_name = Column(String(150), nullable=True)
    department = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)

    eligibility_checks = relationship("EligibilityCheck", back_populates="student")
    scholarship_applications = relationship(
        "ScholarshipApplication", back_populates="student"
    )
    recipients = relationship("ScholarshipRecipient", back_populates="student")
    chat_history = relationship("ChatHistory", back_populates="student")


class EligibilityCheck(Base):
    __tablename__ = "eligibility_checks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    scholarship_id = Column(
        Integer, ForeignKey("scholarships.id"), nullable=True
    )  # Null for general check
    eligible_scholarships = Column(JSON)  # List of eligible scholarship IDs
    check_data = Column(JSON)  # Student data used for checking
    result_summary = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="eligibility_checks")


class ScholarshipApplication(Base):
    __tablename__ = "scholarship_applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, approved, rejected
    documents_submitted = Column(JSON)
    notes = Column(Text)
    applied_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="scholarship_applications")
    scholarship = relationship("Scholarship")


class ScholarshipRecipient(Base):
    __tablename__ = "scholarship_recipients"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id"), nullable=False)
    academic_year = Column(String(20))  # e.g., "2024-2025"
    amount_disbursed = Column(Float)
    status = Column(String(50), default="disbursed")  # disbursed, pending
    disbursed_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="recipients")
    scholarship = relationship("Scholarship", back_populates="recipients")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context_used = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="chat_history")
