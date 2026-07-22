from typing import List, Dict, Any
from pydantic import BaseModel

class DashboardMetrics(BaseModel):
    total_leads: int
    active_campaigns: int
    signals_detected_today: int
    emails_sent_today: int
    meetings_booked_month: int

class FunnelMetrics(BaseModel):
    stages: Dict[str, int]
    conversion_rates: Dict[str, float]

class SignalPerformance(BaseModel):
    signal_type: str
    count: int
    conversion_rate: float

class TimelineDataPoint(BaseModel):
    date: str
    value: int

class TimelineData(BaseModel):
    metric: str
    data: List[TimelineDataPoint]
