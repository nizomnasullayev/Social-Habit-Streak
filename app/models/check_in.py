from datetime import datetime, date
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import Date, DateTime, ForeignKey, UniqueConstraint, func
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.habit import Habit

class CheckIn(Base):
    __tablename__="check_ins"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    habit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
    habit: Mapped["Habit"] = relationship(back_populates="check_ins")
    checked_on: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__=(UniqueConstraint("habit_id", "checked_on"),)