from typing import Dict, Any, Tuple
from app.services.personalization.spintax import SpintaxParser

class DeterministicWriter:
    """Zero-Cost 'AI' Engine using heuristic template mapping and Spintax."""
    
    TEMPLATES = {
        "topic_intent": {
            "subject": "[[quick question|thoughts|idea]] regarding your [[post|comment]] in r/{subreddit}",
            "body": "[[Hi|Hello|Hey]] {author},\n\n[[I saw|Just noticed|Came across]] your recent post about {title}.\n\n[[Since you're looking for solutions|Given what you mentioned|Since this is a common pain point]], I thought I'd reach out. Our platform natively handles exactly this by [[automating the workflow|streamlining the process|eliminating the manual work]].\n\n[[Would you be open to a quick chat?|Worth exploring?|Open to comparing notes?]]\n\nBest,\nAlex"
        },
        "job_change": {
            "subject": "[[congrats|congratulations]] on the new role at {company_name}",
            "body": "[[Hi|Hey]] {author},\n\n[[Massive congrats|Congratulations|Great to see you step]] into the new role at {company_name}.\n\n[[Usually, new leaders|Most executives|Often, leaders]] evaluate their tech stack in the first 90 days. If you're looking to [[boost efficiency|scale outbound|improve pipeline]], we just launched a new playbook for teams like {company_name}.\n\n[[Let me know if you want to take a look.|Worth a quick look?|Interested in checking it out?]]\n\nCheers,\nAlex"
        },
        "default": {
            "subject": "[[quick question|exploring synergies|quick thought]] for {company_name}",
            "body": "[[Hi|Hello|Hey]] {author},\n\n[[I hope you're having a great week.|Hope you're doing well.|Hope all is well.]]\n\nWe help companies like {company_name} [[generate more pipeline|scale their outreach|improve conversion rates]] using signal-driven automation.\n\n[[Open to a 5-min chat?|Would you be against a quick intro?|Worth a brief conversation?]]\n\nBest,\nAlex"
        }
    }

    @classmethod
    def generate_draft(cls, signal_type: str, context: Dict[str, Any]) -> Tuple[str, str]:
        """Generate a highly contextual, unique email draft using Spintax."""
        template_set = cls.TEMPLATES.get(signal_type, cls.TEMPLATES["default"])
        
        subject = SpintaxParser.render(template_set["subject"], context)
        body = SpintaxParser.render(template_set["body"], context)
        
        return subject, body
