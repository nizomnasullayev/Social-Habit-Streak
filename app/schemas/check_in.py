import uuid
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class CheckInRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    habit_id: uuid.UUID
    checked_on: date
    created_at: datetime