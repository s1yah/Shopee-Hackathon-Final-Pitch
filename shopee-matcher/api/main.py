from fastapi import FastAPI, HTTPException
from core.models.schemas import MatchRequest, MatchResponse
from pipeline_a.matcher import LiveMatcher

app = FastAPI(title="Shopee Live Matcher API", version="1.0.0")
matcher = LiveMatcher()

@app.post("/match", response_model=MatchResponse)
async def match_shops(request: MatchRequest):
    """
    Endpoint to evaluate if two shop entries refer to the same entity.
    """
    try:
        result = await matcher.process(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
