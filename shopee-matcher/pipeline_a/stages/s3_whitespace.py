import re
from core.models.schemas import MatchRequest

def run(request: MatchRequest) -> tuple[str, str]:
    """
    Stage 3: Whitespace Removal
    Normalizes the strings for the fuzzy matcher by removing whitespace and special chars.
    """
    def clean(s: str) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', s.lower())

    return clean(request.shop_a_name), clean(request.shop_b_name)
