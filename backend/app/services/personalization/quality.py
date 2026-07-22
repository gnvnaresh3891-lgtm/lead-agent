class QualityChecker:
    def check_quality(self, email_content: dict) -> dict:
        body_length = len(email_content.get("body", ""))
        
        issues = []
        if body_length > 1000:
            issues.append("Email is too long, might impact deliverability.")
        if body_length < 50:
            issues.append("Email is too short, might seem spammy.")
            
        score = 100.0
        score -= len(issues) * 10
        
        return {
            "score": max(0.0, score),
            "is_approved": score >= 80,
            "issues": issues
        }
