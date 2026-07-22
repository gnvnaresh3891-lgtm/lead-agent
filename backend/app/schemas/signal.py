from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class SignalBase(BaseModel):
    type: str
    description: str
    source: str
    metadata: Optional[Dict[str, Any]] = None

class SignalCreate(SignalBase):
    lead_id: Optional[str] = None
    company_name: Optional[str] = None

class SignalResponse(SignalBase):
    id: str
    lead_id: Optional[str] = None
    score_impact: float
    detected_at: datetime

    class Config:
        from_attributes = True

class SignalFeedResponse(BaseModel):
    items: List[SignalResponse]
    total: int

class SignalStats(BaseModel):
    total_signals: int
    signals_by_type: Dict[str, int]
    average_score_impact: float
