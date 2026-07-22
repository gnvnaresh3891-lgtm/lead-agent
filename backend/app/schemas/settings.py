from typing import List, Optional
from pydantic import BaseModel

class ICPConfig(BaseModel):
    target_industries: List[str]
    company_size_min: int
    company_size_max: int
    target_roles: List[str]
    excluded_keywords: List[str]

class DomainStatus(BaseModel):
    domain: str
    is_verified: bool
    dkim_status: str
    spf_status: str
    dmarc_status: str
    health_score: float

class IntegrationStatus(BaseModel):
    name: str
    is_connected: bool
    last_sync: Optional[str] = None
    error_message: Optional[str] = None
