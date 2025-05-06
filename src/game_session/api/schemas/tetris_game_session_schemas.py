from pydantic import BaseModel, Field
from typing import List, Optional, Union
from uuid import UUID
from datetime import datetime


class TetrominoType(str):
    """Enum-like type for Tetromino types."""
    I = "I"
    J = "J"
    L = "L"
    O = "O"
    S = "S"
    T = "T"
    Z = "Z"


class Tetromino(BaseModel):
    type: TetrominoType
    matrix: List[List[bool]]
    color: str


class Position(BaseModel):
    x: int
    y: int


class CurrentPiece(BaseModel):
    tetromino: Tetromino
    position: Position


class GameStatus(str):
    """Enum-like type for game statuses."""
    ACTIVE = "active"
    PAUSED = "paused"
    GAMEOVER = "gameover"


class TetrisGameSessionBase(BaseModel):
    field_width: int = Field(default=10, ge=1, le=40)
    field_height: int = Field(default=20, ge=1, le=80)
    grid: List[List[bool]]
    colors: List[List[str]]
    next_pieces: List[TetrominoType]
    current_piece: Optional[CurrentPiece] = None
    score: int = Field(default=0, ge=0)
    level: int = Field(default=1, ge=1)
    lines_cleared: int = Field(default=0, ge=0)
    status: GameStatus
    last_updated: datetime


class TetrisGameSessionCreate(TetrisGameSessionBase):
    """Schema for creating a TetrisGameSession."""
    player_id: int  # Assuming player_id is an int , needs to be changed for a string (UUID or username)


class TetrisGameSessionUpdate(BaseModel):
    """Schema for updating a TetrisGameSession."""
    field_width: Optional[int] = Field(None, ge=1, le=40)
    field_height: Optional[int] = Field(None, ge=1, le=80)
    grid: Optional[List[List[bool]]] = None
    colors: Optional[List[List[str]]] = None
    next_pieces: Optional[List[TetrominoType]] = None
    current_piece: Optional[Union[CurrentPiece, None]] = None
    score: Optional[int] = Field(None, ge=0)
    level: Optional[int] = Field(None, ge=1)
    lines_cleared: Optional[int] = Field(None, ge=0)
    status: Optional[GameStatus] = None


class TetrisGameSession(TetrisGameSessionBase):
    """Schema for reading a TetrisGameSession."""
    id: UUID
    player_id: str

    class Config:
        orm_mode = True