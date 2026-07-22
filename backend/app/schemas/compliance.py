from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ComplianceCheckResponse(BaseModel):
    is_compliant: bool
    reasons: List[str]
    checked_at: datetime

class SuppressionBase(BaseModel):
    target: str # Email or domain
    type: str # 'email', 'domain'
    reason: str

class SuppressionCreate(SuppressionBase):
    pass

class SuppressionResponse(SuppressionBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        from_attributes = True

class ComplianceStats(BaseModel):
    total_suppressed: int
    recent_violations: int
    suppression_by_type: dict
