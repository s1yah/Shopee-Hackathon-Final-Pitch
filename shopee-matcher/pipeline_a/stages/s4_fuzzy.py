from thefuzz import fuzz

def run(normalized_a: str, normalized_b: str) -> float:
    """
    Stage 4: Fuzzy Distance Scoring
    Returns a score between 0 and 100 based on the similarity of the normalized strings.
    """
    if not normalized_a or not normalized_b:
        return 0.0
    return float(fuzz.ratio(normalized_a, normalized_b))
