def classify_intent(text: str) -> str:
    text = text.lower() if text else ""
    if "unsubscribe" in text or "stop" in text or "remove me" in text:
        return "opt_out"
    if "interested" in text or "tell me more" in text or "call" in text:
        return "positive"
    if "not interested" in text or "no thanks" in text:
        return "negative"
    if "later" in text or "busy" in text:
        return "later"
    return "unknown"
