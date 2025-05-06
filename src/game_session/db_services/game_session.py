import fastapi
import sqlalchemy
from sqlalchemy.future import select

from src.core.db import BaseService
from src.game_session.models import TetrisGameSession
from src.game_session.api.schemas import TetrisGameSession, TetrisGameSessionCreate, TetrisGameSessionUpdate

class TetrisGameSessionCRUDService(BaseService):
    """CRUD service for TetrisGameSession."""

    async def create(
        self,
        session_data: TetrisGameSessionCreate,
    ) -> TetrisGameSession:
        """Create a new Tetris game session."""
        session = TetrisGameSession(**session_data.model_dump())
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return TetrisGameSession.model_validate(session)

    async def get_list(
        self,
        offset: int,
        size: int,
    ) -> dict:
        """Get list of Tetris game sessions."""
        query = select(TetrisGameSession).offset(offset).limit(size)
        sessions = await self.session.execute(query)
        total_count = await self.session.execute(
            select(sqlalchemy.func.count("*")).select_from(TetrisGameSession)
        )
        return {
            "sessions": [
                TetrisGameSession.model_validate(record[0])
                for record in sessions.fetchall()
            ],
            "total_count": total_count.scalar(),
        }

    async def get_one(
        self,
        session_id: str,
    ) -> TetrisGameSession:
        """Get a single Tetris game session."""
        session = await self.session.get(TetrisGameSession, session_id)
        if not session:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Tetris game session not found.",
            )
        return TetrisGameSession.model_validate(session)

    async def update(
        self,
        session_id: str,
        update_data: TetrisGameSessionUpdate,
    ) -> TetrisGameSession:
        """Update an existing Tetris game session."""
        session = await self.session.get(TetrisGameSession, session_id)
        if not session:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Tetris game session not found.",
            )
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(session, key, value)
        await self.session.commit()
        await self.session.refresh(session)
        return TetrisGameSession.model_validate(session)

    async def delete(self, session_id: str) -> None:
        """Delete a Tetris game session."""
        session = await self.session.get(TetrisGameSession, session_id)
        if not session:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Tetris game session not found.",
            )
        await self.session.delete(session)
        await self.session.commit()