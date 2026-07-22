def detect_jurisdiction(location: str) -> str:
    location = location.lower() if location else ""
    if "california" in location or "ca" in location:
        return "CCPA"
    elif "uk" in location or "united kingdom" in location or "europe" in location:
        return "GDPR"
    return "CAN-SPAM"

def can_send(lead, jurisdiction: str) -> bool:
    if jurisdiction == "GDPR":
        return getattr(lead, "has_opted_in", False)
    elif jurisdiction == "CCPA":
        return not getattr(lead, "has_opted_out", False)
    return not getattr(lead, "has_opted_out", False)
