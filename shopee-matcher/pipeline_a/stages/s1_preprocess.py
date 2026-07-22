import re
from core.models.schemas import MatchRequest, MatchResponse

def run(request: MatchRequest) -> MatchResponse | None:
    """
    Stage 1: Preprocessing & Direct Match
    Cleans common words (Shop, Store, Official) and checks for direct match.
    """
    def clean_name(name: str) -> str:
        name = name.lower()
        name = re.sub(r'\b(shop|store|official|mall|ph|philippines)\b', '', name)
        return name.strip()

    name_a = clean_name(request.shop_a_name)
    name_b = clean_name(request.shop_b_name)

    if name_a and name_a == name_b:
        return MatchResponse(is_match=True, confidence=1.0, reason="Direct name match after common word removal", stage_resolved=1)
    
    return None
