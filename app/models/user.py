from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import text
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: UUID = Field(
        default_factory=uuid4, 
        primary_key=True, 
        nullable=False
    )
    
    email: str = Field(
        unique=True, 
        index=True, 
        nullable=False
    )
    
    hashed_password: str | None = Field(
        default=None, 
        nullable=True
    )
    
    timezone: datetime = Field(
        sa_column_kwargs={
            "server_default": text("TIMEZONE('utc', now())")
        }
    )   