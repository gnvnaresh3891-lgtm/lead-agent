from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime

class LeadBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    company_name: str
    job_title: Optional[str] = None
    linkedin_url: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None

class LeadResponse(LeadBase):
    id: str
    status: str
    score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LeadListResponse(BaseModel):
    items: List[LeadResponse]
    total: int
    page: int
    size: int

class PipelineResponse(BaseModel):
    new_leads: int
    contacted: int
    qualified: int
    closed_won: int
    closed_lost: int
