from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, Params

from src.rating.services.score_service import ScoreService
from src.rating.exceptions import (
    NotFoundError,
    InvalidScoreError,
    PaginationError,
)
from src.rating.schemas.scores import ScoreResponse, LeaderboardResponse

router = APIRouter()

def handle_service_errors(func):
    """Decorator to convert service exceptions to HTTP responses."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except InvalidScoreError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except PaginationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail="Internal server error")
    return wrapper

@router.post("/users/{user_id}/scores", response_model=ScoreResponse)
@handle_service_errors
async def submit_score(
    user_id: int,
    score: int

):
    async with ScoreService() as service:
        await service.submit_score(user_id, score)
        return {"message": "Score submitted successfully"}

@router.get("/users/{user_id}/scores", response_model=Page[ScoreResponse])
@handle_service_errors
async def get_user_scores(
    user_id: int,
    params: Params = Depends()
):
    async with ScoreService() as service:
        result = await service.get_user_scores(
            user_id,
            offset=params.offset,
            limit=params.limit
        )
        return {
            "items": result["scores"],
            "total": result["total_count"],
            "offset": params.offset,
            "limit": params.limit,
        }

@router.get("/leaderboard/highscores", response_model=LeaderboardResponse)
@handle_service_errors
async def get_highscore_leaderboard(
    params: Params = Depends()
):
    async with ScoreService() as service:
        result = await service.get_highscore_leaderboard(
            offset=params.offset,
            limit=params.limit
        )
        return {
            "items": result["leaderboard"],
            "total": result["total_count"],
            "offset": params.offset,
            "limit": params.limit,
        }