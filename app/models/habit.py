from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class Habit(SQLModel, table=True):
    __tablename__ = "habits"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )

    user_uid: UUID = Field(
        foreign_key="users.uid",
        nullable=False
    )

    name: str = Field(
        nullable=False
    )

    is_custom: bool = Field(
        default=False
    )

    frequency: str = Field(
        default="daily"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    is_active: bool = Field(
        default=True
    )