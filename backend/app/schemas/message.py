from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    lead_id: str
    campaign_id: Optional[str] = None
    subject: str
    body: str
    channel: str = "email"

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    status: str
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class GenerateEmailRequest(BaseModel):
    lead_id: str
    context_data: Optional[Dict[str, Any]] = None

class GenerateEmailResponse(BaseModel):
    subject: str
    body: str
    model_used: str
    confidence_score: float
