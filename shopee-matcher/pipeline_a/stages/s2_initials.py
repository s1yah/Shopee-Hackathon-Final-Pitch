import re
from core.models.schemas import MatchRequest, MatchResponse

def run(request: MatchRequest) -> MatchResponse | None:
    """
    Stage 2: Acronym / Initials CPU Guard
    Checks if one name is just the initials of the other.
    """
    def get_initials(name: str) -> str:
        return "".join([word[0] for word in re.findall(r'\b\w', name.lower())])

    name_a = request.shop_a_name.lower().strip()
    name_b = request.shop_b_name.lower().strip()

    initials_a = get_initials(name_a)
    initials_b = get_initials(name_b)

    if (len(name_a) > 3 and name_b == initials_a) or (len(name_b) > 3 and name_a == initials_b):
        return MatchResponse(is_match=True, confidence=0.9, reason="Initials/Acronym match", stage_resolved=2)

    return None
