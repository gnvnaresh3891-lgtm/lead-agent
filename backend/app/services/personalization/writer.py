import random

class MockEmailWriter:
    def __init__(self):
        self.templates = {
            "champion_job_change": [
                "Hi {first_name}, saw you recently joined {company_name}. I know we had great success at your last company, would love to see if we can replicate it here.",
                "Congrats on the new role at {company_name}, {first_name}! Wondering if {topic} is on your radar yet?"
            ],
            "multi_stakeholder_visit": [
                "Hi {first_name}, noticed a few folks from {company_name} checking out our site. Are you evaluating {topic}?",
                "Hey {first_name}, looks like your team is doing some research. Happy to share how we help companies like yours."
            ],
            "new_leadership": [
                "Welcome to the new leadership team at {company_name}, {first_name}. Often, this means new initiatives. Can we chat about {topic}?",
                "Hi {first_name}, with the recent leadership changes, is {topic} becoming a priority?"
            ],
            "competitor_removal": [
                "Hi {first_name}, noticed you might be moving off of your current solution. We've helped many transition smoothly.",
                "Hey {first_name}, if you're evaluating alternatives to your current stack, I'd love to show you our platform."
            ],
            "job_posting": [
                "Hi {first_name}, I saw {company_name} is hiring for {role}. We typically help teams in this phase streamline operations.",
                "Looks like your team is growing! With the new {role} role, how are you handling {topic}?"
            ],
            "funding": [
                "Huge congrats on the recent round, {first_name}! What's the main focus for the new capital?",
                "Hi {first_name}, saw the funding news. Are you planning to invest in {topic} to accelerate growth?"
            ],
            "sec_filing": [
                "Hi {first_name}, noticed the recent filing mentioning {topic}. We specialize in addressing these exact challenges.",
                "Hey {first_name}, based on your recent 10-K, it looks like efficiency is a big theme. Can we help?"
            ],
            "hiring_surge": [
                "Hi {first_name}, {company_name} is growing incredibly fast. How are you maintaining {topic} at this scale?",
                "Wow, so many open roles! We help scaling teams handle {topic} without dropping the ball."
            ],
            "topic_intent": [
                "Hi {first_name}, looks like you've been researching {topic}. We're experts in this area. Care to chat?",
                "Hey {first_name}, if {topic} is top of mind, I have some resources that might help."
            ],
            "website_visit": [
                "Hi {first_name}, thanks for stopping by our site. Were you able to find what you were looking for?",
                "Hey {first_name}, noticed you checking out our resources. Can I point you in the right direction?"
            ],
            "tech_change": [
                "Hi {first_name}, saw you recently added {tech} to your stack. We integrate beautifully with it.",
                "Hey {first_name}, if you're implementing {tech}, you might be interested in how we complement it."
            ],
            "job_change": [
                "Congrats on the new position, {first_name}! Let's connect on how we can help you hit the ground running.",
                "Hi {first_name}, new role, new tools? Let me show you how we can make your life easier."
            ],
            "general": [
                "Hi {first_name}, wanted to see if {topic} is a priority for {company_name} this quarter.",
                "Hey {first_name}, we help teams like yours achieve {goal}. Worth a chat?",
                "Hi {first_name}, reaching out to see if you're exploring solutions for {topic}."
            ]
        }
        
    def generate_email(self, context: dict) -> dict:
        signal_type = "general"
        signals = context.get("recent_signals", [])
        if signals:
            signal_type = signals[0].get("type", "general")
            
        lead = context.get("lead", {})
        
        templates = self.templates.get(signal_type, self.templates["general"])
        template = random.choice(templates)
        
        body = template.format(
            first_name=lead.get("first_name", "there"),
            company_name=lead.get("company_name", "your company"),
            topic="this area",
            role="these roles",
            tech="this tool",
            goal="your goals"
        )
        
        return {
            "subject": f"Thoughts on {lead.get('company_name', 'your company')}?",
            "body": body,
            "model_used": "mock-writer-v1",
            "confidence_score": round(random.uniform(0.7, 0.99), 2)
        }
