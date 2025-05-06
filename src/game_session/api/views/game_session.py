from fastapi import APIRouter, Query, status
from src.game_session.db_services import TetrisGameSessionCRUDService
from src.game_session.api.schemas import (
    TetrisGameSession,
    TetrisGameSessionCreate,
    TetrisGameSessionUpdate,
)

router = APIRouter(prefix="/game-sessions", tags=["Tetris Game Sessions"])


@router.post("/", response_model=TetrisGameSession, status_code=status.HTTP_201_CREATED)
async def create_game_session(session_data: TetrisGameSessionCreate):
    """Create a new Tetris game session."""
    async with TetrisGameSessionCRUDService() as service:
        return await service.create(session_data)


@router.get("/", response_model=dict)
async def list_game_sessions(
    offset: int = Query(0, ge=0),
    size: int = Query(10, gt=0, le=100)
):
    """Get a paginated list of Tetris game sessions."""
    async with TetrisGameSessionCRUDService() as service:
        return await service.get_list(offset, size)


@router.get("/{session_id}", response_model=TetrisGameSession)
async def get_game_session(session_id: str):
    """Retrieve a single Tetris game session by ID."""
    async with TetrisGameSessionCRUDService() as service:
        return await service.get_one(session_id)


@router.put("/{session_id}", response_model=TetrisGameSession)
async def update_game_session(session_id: str, update_data: TetrisGameSessionUpdate):
    """Update an existing Tetris game session."""
    async with TetrisGameSessionCRUDService() as service:
        return await service.update(session_id, update_data)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game_session(session_id: str):
    """Delete a Tetris game session."""
    async with TetrisGameSessionCRUDService() as service:
        await service.delete(session_id)