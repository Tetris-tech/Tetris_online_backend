import sqlalchemy
from sqlalchemy import Column, DateTime, String

from src.config.database import BaseModel

class RevokedToken(BaseModel):

    __tablename__ = 'revoked_tokens'

    refresh_token = Column(String,unique=True,nullable=False)
    expires_at = Column(DateTime,nullable=False)

    # CheckConstraint ensures expires_at is not before added_at and is not in the past
    __table_args__ = (
        sqlalchemy.Index('idx_refresh_token', 'refresh_token'),
        sqlalchemy.CheckConstraint(
            "expires_at >= created",  # Ensure expires_at is later than added_at
            name="expires_later_than_added"
        ),
    )
    def __repr__(self):
        return f"<RevokedToken(id={self.id}, refresh_token={self.refresh_token}, added_at={self.created}, expires_at={self.expires_at})>"
