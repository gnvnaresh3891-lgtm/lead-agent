from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str
    target_criteria: dict

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    target_criteria: Optional[dict] = None

class CampaignResponse(CampaignBase):
    id: str
    created_at: datetime
    updated_at: datetime
    leads_count: int

    class Config:
        from_attributes = True

class CampaignListResponse(BaseModel):
    items: List[CampaignResponse]
    total: int
