from datetime import date, datetime
from uuid import uuid4, UUID

from sqlmodel import Field, SQLModel

class HabitLog(SQLModel, table=True):

    __tablename__ = "habit_logs"

    uid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )

    habit_uid: UUID = Field(
        foreign_key="habits.uid",
        nullable=False  
    )

    user_uid: UUID = Field(
        foreign_key="users.uid",
        nullable=False
    )

    checked_in_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    local_date: date