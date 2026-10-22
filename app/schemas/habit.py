from datetime import datetime
import uuid
from pydantic import BaseModel, Field, ConfigDict

class HabitCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=50)
    description: str | None = Field(max_length=500, default=None)

class HabitUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str | None = Field(min_length=1, max_length=50, default=None)
    description: str | None = Field(max_length=500, default=None)
    is_archived: bool | None = None

class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    description: str | None
    is_archived: bool
    created_at: datetime