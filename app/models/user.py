from datetime import datetime
import uuid
from app.database import Base
from sqlalchemy import UUID, Column, String, func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__="users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, default=None)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(250))
    avatar: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=True, onupdate=func.now()
    )