from core.models.schemas import MatchRequest, MatchResponse, RuleStatus, Rule
from pipeline_a.stages import s1_preprocess, s2_initials, s3_whitespace, s4_fuzzy, s5_clip, s7_vision_llm

class LiveMatcher:
    def __init__(self):
        # Initialize models (CLIP, LLM, etc.) here if not mocked
        pass

    async def process(self, request: MatchRequest) -> MatchResponse:
        """
        Runs the cascading pipeline on an incoming pair of shop names/logos.
        """
        # Stage 1: Preprocessing (Direct match, Regex)
        result1 = s1_preprocess.run(request)
        if result1: return result1

        # Stage 2: Acronym / Initials Guard
        result2 = s2_initials.run(request)
        if result2: return result2

        # Stage 3: Whitespace Removal (Normalizing)
        normalized_a, normalized_b = s3_whitespace.run(request)

        # Stage 4: Fuzzy Distance Scoring
        score = s4_fuzzy.run(normalized_a, normalized_b)
        if score >= 85: 
            return MatchResponse(is_match=True, confidence=score/100.0, reason="High fuzzy match", stage_resolved=4)
        if score <= 40: 
            return MatchResponse(is_match=False, confidence=1.0 - (score/100.0), reason="Low fuzzy match", stage_resolved=4)

        # Stage 5: Visual Pre-filter (CLIP)
        logo_sim = await s5_clip.run(str(request.shop_a_logo_url) if request.shop_a_logo_url else None, 
                                     str(request.shop_b_logo_url) if request.shop_b_logo_url else None)
        if logo_sim >= 0.9: 
            return MatchResponse(is_match=True, confidence=logo_sim, reason="High logo similarity", stage_resolved=5)
        if logo_sim <= 0.2: 
            return MatchResponse(is_match=False, confidence=1.0 - logo_sim, reason="Low logo similarity", stage_resolved=5)

        # Stage 6: Selective Rule Retrieval (Mocked for now)
        # In a real system, we'd query the DB for ACTIVE rules
        active_rules = [
            Rule(id=1, description="Same shop name, different branch location", status=RuleStatus.ACTIVE)
        ]

        # Stage 7: Vision-LLM Judgment
        final_decision = await s7_vision_llm.run(request, active_rules)
        return final_decision
