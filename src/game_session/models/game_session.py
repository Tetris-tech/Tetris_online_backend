import uuid
from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    ForeignKey,
    Enum,
    JSON,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Enums
class GameStatusEnum(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    GAMEOVER = "gameover"


class TetrominoKindEnum(str, Enum):
    I = "I"
    J = "J"
    L = "L"
    O = "O"
    S = "S"
    T = "T"
    Z = "Z"

# Models

class TetrisGameSession(Base):
    __tablename__ = "tetris_game_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    field_width = Column(SmallInteger, nullable=False, default=10)
    field_height = Column(SmallInteger, nullable=False, default=20)
    grid = Column(JSON, nullable=False)  # Representing boolean[][] as JSON
    colors = Column(JSON, nullable=False)  # Representing varchar(7)[][] as JSON
    current_piece = Column(
        JSON,
        nullable=True,
        comment=(
            "Embedded Tetromino + Position. Example: "
            "{tetromino: {type: , matrix: [[]], color: }, position: {x: 0, y: 0}}"
        ),
    )
    next_pieces = Column(ARRAY(Enum(TetrominoKindEnum)), nullable=False)
    score = Column(Integer, nullable=False, default=0)
    level = Column(Integer, nullable=False, default=1)
    lines_cleared = Column(Integer, nullable=False, default=0)
    status = Column(Enum(GameStatusEnum), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())