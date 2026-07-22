from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from enum import Enum

class RuleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    MIGRATED = "MIGRATED"

class Rule(BaseModel):
    id: int
    description: str
    status: RuleStatus

class MatchRequest(BaseModel):
    shop_a_name: str
    shop_a_logo_url: Optional[HttpUrl] = None
    shop_b_name: str
    shop_b_logo_url: Optional[HttpUrl] = None

class MatchResponse(BaseModel):
    is_match: bool
    confidence: float
    reason: str
    stage_resolved: int
