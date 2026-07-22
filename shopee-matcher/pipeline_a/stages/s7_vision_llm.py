import random
from typing import List
from core.models.schemas import MatchRequest, MatchResponse, Rule

async def run(request: MatchRequest, rules: List[Rule]) -> MatchResponse:
    """
    Stage 7: Vision-LLM Judgment
    MOCK IMPLEMENTATION: Simulates passing context to an LLM for final judgment.
    """
    # In reality:
    # prompt = build_prompt(request, rules)
    # response = llm.predict(prompt)
    # return parse_llm_response(response)
    
    # Mock behavior: Randomly decide, but lean towards match if certain keywords exist
    rules_text = ", ".join([r.description for r in rules])
    is_match = random.choice([True, False])
    reason = f"Based on LLM analysis incorporating rules: {rules_text}" if rules else "Based on LLM analysis without specific rules."
    
    return MatchResponse(is_match=is_match, confidence=0.85, reason=reason, stage_resolved=7)
