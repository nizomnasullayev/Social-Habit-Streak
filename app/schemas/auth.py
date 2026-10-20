from pydantic import BaseModel
from pydantic import EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RegisterRequest(BaseModel):
    username: str | None = Field(default=None, max_length=255)
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"