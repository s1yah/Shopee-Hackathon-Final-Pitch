import random
from typing import Optional

async def run(logo_url_a: Optional[str], logo_url_b: Optional[str]) -> float:
    """
    Stage 5: Visual Pre-filter (CLIP)
    MOCK IMPLEMENTATION: Simulates downloading images and computing cosine similarity via CLIP.
    """
    if not logo_url_a or not logo_url_b:
        return 0.0
    
    if logo_url_a == logo_url_b:
        return 1.0
        
    # In reality: 
    # image_a = download(logo_url_a)
    # image_b = download(logo_url_b)
    # features_a = clip_model.encode(image_a)
    # features_b = clip_model.encode(image_b)
    # return cosine_similarity(features_a, features_b)
    
    # Mocking a similarity score between 0.3 and 0.95
    return random.uniform(0.3, 0.95)
