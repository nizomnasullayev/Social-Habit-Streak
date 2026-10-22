from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, func
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.check_in import CheckIn


class Habit(Base):
    __tablename__="habits"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="habits")
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(500), default=None)
    is_archived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    check_ins: Mapped[list["CheckIn"]] = relationship(back_populates="habit", cascade="all, delete-orphan")