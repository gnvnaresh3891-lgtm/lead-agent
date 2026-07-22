import math
from datetime import datetime

SIGNAL_WEIGHTS = {
    "champion_job_change": 95,
    "multi_stakeholder_visit": 90,
    "new_leadership": 80,
    "competitor_removal": 75,
    "job_posting": 60,
    "funding": 55,
    "sec_filing": 50,
    "hiring_surge": 45,
    "topic_intent": 20,
    "website_visit": 65,
    "tech_change": 70,
    "job_change": 85
}

DECAY_LAMBDA = 0.05

def calculate_signal_score(signal_type: str, detected_at: datetime) -> float:
    base_score = SIGNAL_WEIGHTS.get(signal_type, 10)
    days_elapsed = (datetime.utcnow() - detected_at).days
    if days_elapsed < 0:
        days_elapsed = 0
    
    decayed_score = base_score * math.exp(-DECAY_LAMBDA * days_elapsed)
    return max(0.0, min(100.0, decayed_score))

def calculate_icp_fit(lead_data: dict, icp_config: dict) -> float:
    score = 50.0
    
    if lead_data.get("industry") in icp_config.get("target_industries", []):
        score += 20.0
        
    company_size = lead_data.get("company_size", 0)
    if icp_config.get("company_size_min", 0) <= company_size <= icp_config.get("company_size_max", float('inf')):
        score += 20.0
        
    if lead_data.get("role") in icp_config.get("target_roles", []):
        score += 10.0
        
    return min(100.0, score)

def calculate_composite_score(signal_score: float, icp_score: float) -> float:
    # 60% weight to signals, 40% to ICP fit
    return (signal_score * 0.6) + (icp_score * 0.4)

def get_score_tier(score: float) -> str:
    if score >= 80:
        return "Tier 1 (High Intent)"
    elif score >= 50:
        return "Tier 2 (Medium Intent)"
    else:
        return "Tier 3 (Low Intent)"
