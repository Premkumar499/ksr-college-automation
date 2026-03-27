from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Scholarship Schemas
class ScholarshipBase(BaseModel):
    name: str
    provider: Optional[str] = None
    description: Optional[str] = None
    eligibility_criteria: Dict[str, Any]
    documents_required: List[str]
    application_procedure: Optional[str] = None
    deadline: Optional[datetime] = None
    amount: Optional[float] = None


class ScholarshipCreate(ScholarshipBase):
    pass


class ScholarshipResponse(ScholarshipBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Student Schemas
class StudentBase(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    year: Optional[int] = None
    gpa: Optional[float] = None
    category: Optional[str] = None
    family_income: Optional[float] = None
    gender: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Eligibility Schemas
class EligibilityCheckRequest(BaseModel):
    student_id: Optional[int] = None
    student_data: Optional[StudentCreate] = None  # If not registered


class EligibilityScholar(BaseModel):
    scholarship_id: int
    scholarship_name: str
    eligibility_score: float = Field(ge=0, le=100)
    reasons: List[str]


class EligibilityCheckResponse(BaseModel):
    eligible_scholarships: List[EligibilityScholar]
    total_found: int
    check_id: Optional[int] = None


# Chat Schemas
class ChatRequest(BaseModel):
    query: str
    student_id: Optional[int] = None
    conversation_history: Optional[List[Dict[str, str]]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.conversation_history is None:
            self.conversation_history = []


class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []
    conversation_id: str


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_scholarships: int
    total_eligible_students: int
    total_applications: int
    total_disbursed_amount: float


class ScholarshipStats(BaseModel):
    scholarship_id: int
    scholarship_name: str
    total_recipients: int
    total_amount_disbursed: float
    average_gpa: Optional[float]


class RecipientInfo(BaseModel):
    student_id: str
    student_name: str
    department: str
    scholarship_name: str
    amount: float
    academic_year: str


class DashboardResponse(BaseModel):
    stats: DashboardStats
    scholarship_breakdown: List[ScholarshipStats]
    recent_recipients: List[RecipientInfo]
