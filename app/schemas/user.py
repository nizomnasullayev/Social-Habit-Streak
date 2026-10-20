from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    email: str
    username: str | None
    avatar: str | None
    created_at: datetime