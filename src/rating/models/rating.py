
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.core.models import BaseModel


class GameScore(BaseModel):
    __tablename__ = "game_scores"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)  # Tetris score from a single game session

    user = relationship("User", backref="scores")