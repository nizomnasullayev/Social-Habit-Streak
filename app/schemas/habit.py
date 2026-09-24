from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class HabitCreate(BaseModel):
    name: str
    frequency: str = "daily"


class HabitRead(BaseModel):
    uid: UUID
    user_uid: UUID
    name: str
    is_custom: bool
    frequency: str
    created_at: datetime
    is_active: bool