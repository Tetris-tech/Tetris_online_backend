import hashlib
from datetime import datetime, timezone

import sqlalchemy

from src.friend.api.schemas import FriendStatus
from src.core.models import BaseModel


class Friend(BaseModel): #TODO: since models now belong to a api package, might be a good idea to move it to friend api?
    """Model to save friend relations."""

    __tablename__ = "friend"
# TODO: add indexes on sender_id and recipient_id (or use a materialized view)
    sender_id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        sqlalchemy.ForeignKey("users.id"),
        name="sender_id",
    )
    recipient_id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        sqlalchemy.ForeignKey("users.id"),
        name="recipient_id",
    )
    status = sqlalchemy.Column(
        sqlalchemy.Enum(FriendStatus),
        default=FriendStatus.PENDING,
        nullable=False,
        name="status"
    )
    # Column to track the friendship duration, i.e. when friendship got accepted
    # TODO: Add corresponding logic
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.now(timezone.utc),
        name="created_at"
    )

    __table_args__ = (
        sqlalchemy.CheckConstraint(
            "sender_id != recipient_id",
            name="user_cannot_add_itself",
        ),
        sqlalchemy.UniqueConstraint("sender_id", "recipient_id"),
    )


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    username = sqlalchemy.Column(
        sqlalchemy.VARCHAR(255),
        name="username",
        nullable=False,
        unique=True,
        index=True,
    )
    password = sqlalchemy.Column(
        sqlalchemy.VARCHAR(255),
        name="password",
        nullable=False,
    )
    rating = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        name="rating",
        default=0,
    )
    is_active = sqlalchemy.Column(
        sqlalchemy.Boolean,
        name="is_active",
        default=False,
    )
    friends = sqlalchemy.orm.relationship(
        "Friend",
        primaryjoin="User.id == Friend.sender_id",
        backref="sender",
        cascade="all, delete-orphan",
    )
    added_by = sqlalchemy.orm.relationship(
        "Friend",
        primaryjoin="User.id == Friend.recipient_id",
        backref="recipient",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        """Set password for user."""
        self.password = self._hash_password(password)

    def check_password(self, password: str) -> bool:
        """Check password matches."""
        return self.password == self._hash_password(password)

    def _hash_password(self, password: str) -> str:
        hashed = hashlib.sha256(password.encode())
        return hashed.hexdigest()
