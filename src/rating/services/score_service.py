from sqlalchemy import func, select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Any

from src.core.db import BaseService
from src.rating.models.rating import GameScore
from src.rating.exceptions import (
    NotFoundError,
    InvalidScoreError,
    PaginationError,
)
from src.user.models import User


class ScoreService(BaseService):
    """Service for score-related operations with error handling."""

    MAX_LIMIT = 100  # Prevent excessive DB load

    async def _validate_user_exists(self, user_id: int) -> None:
        """Check if user exists."""
        user_exists = await self.session.execute(
            select(exists().where(User.id == user_id))
        )
        if not user_exists.scalar():
            raise NotFoundError(f"User {user_id} does not exist")

    async def _validate_pagination(self, offset: int, limit: int) -> None:
        """Validate offset/limit values."""
        if offset < 0 or limit < 1 or limit > self.MAX_LIMIT:
            raise PaginationError(
                f"Invalid pagination: offset={offset}, limit={limit}"
            )

    async def submit_score(self, user_id: int, score: int) -> None:
        """Submit a new score for a user with validation."""
        try:
            # Validate user exists
            await self._validate_user_exists(user_id)

            # Validate score
            if score < 0:
                raise InvalidScoreError("Score cannot be negative")

            # Add score
            new_score = GameScore(user_id=user_id, score=score)
            self.session.add(new_score)
            await self.session.commit()

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError("Database error") from e

    async def get_user_scores(
            self,
            user_id: int,
            offset: int = 0,
            limit: int = 10
    ) -> dict[str, Any]:
        """Get paginated scores for a user with validation."""
        try:
            # Validate user and pagination
            await self._validate_user_exists(user_id)
            await self._validate_pagination(offset, limit)

            # Scores query
            scores_query = (
                select(GameScore)
                .where(GameScore.user_id == user_id)
                .order_by(GameScore.created.desc())
                .offset(offset)
                .limit(limit)
            )
            # Total count query
            count_query = (
                select(func.count(GameScore.id))
                .where(GameScore.user_id == user_id)
            )

            # Execute
            scores_result = await self.session.execute(scores_query)
            count_result = await self.session.execute(count_query)

            return {
                "scores": scores_result.scalars().all(),
                "total_count": count_result.scalar() or 0,
            }

        except SQLAlchemyError as e:
            raise RuntimeError("Database error") from e

    async def get_highscore_leaderboard(
            self,
            offset: int = 0,
            limit: int = 10
    ) -> dict[str, Any]:
        """High score leaderboard with validation."""
        try:
            await self._validate_pagination(offset, limit)

            # Subquery for max scores per user
            subquery = (
                select(
                    GameScore.user_id,
                    func.max(GameScore.score).label("high_score")
                )
                .group_by(GameScore.user_id)
                .subquery()
            )

            # Leaderboard query
            leaderboard_query = (
                select(
                    User.username,
                    subquery.c.high_score)
                .join(subquery, User.id == subquery.c.user_id)
                .order_by(subquery.c.high_score.desc())
                .offset(offset)
                .limit(limit)
            )

            # Total count (users with at least 1 score)
            count_query = select(func.count(subquery.c.user_id))

            # Execute
            leaderboard_result = await self.session.execute(leaderboard_query)
            count_result = await self.session.execute(count_query)

            return {
                "leaderboard": [
                    {"username": row.username, "high_score": row.high_score}
                    for row in leaderboard_result
                ],
                "total_count": count_result.scalar() or 0,
            }

        except SQLAlchemyError as e:
            raise RuntimeError("Database error") from e