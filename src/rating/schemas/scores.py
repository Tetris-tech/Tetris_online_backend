from datetime import datetime

from pydantic import BaseModel

class ScoreResponse(BaseModel):
    id: int
    user_id: int
    score: int
    created_at: datetime

class LeaderboardEntry(BaseModel):
    username: str
    high_score: int

class LeaderboardResponse(BaseModel):
    items: list[LeaderboardEntry]
    total: int
    offset: int
    limit: int