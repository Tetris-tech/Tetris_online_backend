import sqlalchemy

from src.config.database import BaseModel


class Friend(BaseModel):
    """Model to save friend relations."""
    __tablename__ = "friend"

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
    friends = sqlalchemy.orm.relationship(
        "Friend",
        primaryjoin="User.id == Friend.sender_id",
        backref="sender",
        cascade="all, delete-orphan"
    )
    added_by = sqlalchemy.orm.relationship(
        "Friend",
        primaryjoin="User.id == Friend.recipient_id",
        backref="recipient",
        cascade="all, delete-orphan"
    )

