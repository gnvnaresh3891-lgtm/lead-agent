import re
import random
from typing import Dict, Any

class SpintaxParser:
    """Parses and resolves Spintax strings (e.g. '{Hi|Hello} there!'). Supports nesting."""
    
    @staticmethod
    def parse(text: str) -> str:
        """Resolve spintax choices randomly."""
        pattern = re.compile(r'\{([^{}]*)\}')
        while True:
            match = pattern.search(text)
            if not match:
                break
            options = match.group(1).split('|')
            choice = random.choice(options)
            # Replace the outermost matched {group} with the choice
            text = text[:match.start()] + choice + text[match.end():]
        return text

    @staticmethod
    def render(template: str, context: Dict[str, Any]) -> str:
        """First format variables {key}, then resolve Spintax [var1|var2]. 
        Note: To avoid conflict between python format kwargs and Spintax braces,
        we use [[ ]] for spintax in this implementation.
        """
        # Step 1: Inject variables
        # Use safe dictionary formatting in case keys are missing
        class SafeDict(dict):
            def __missing__(self, key):
                return '{' + key + '}'
                
        try:
            formatted_text = template.format_map(SafeDict(**context))
        except Exception:
            formatted_text = template # fallback
            
        # Step 2: Resolve [[a|b|c]] style spintax to avoid collision with {var}
        pattern = re.compile(r'\[\[([^\[\]]*)\]\]')
        while True:
            match = pattern.search(formatted_text)
            if not match:
                break
            options = match.group(1).split('|')
            choice = random.choice(options)
            formatted_text = formatted_text[:match.start()] + choice + formatted_text[match.end():]
            
        return formatted_text
