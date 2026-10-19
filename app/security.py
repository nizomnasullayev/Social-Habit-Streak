import secrets
import uuid
from datetime import datetime, UTC, timedelta
from typing import Any
from app.config import settings
import jwt
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    depracated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(
    subject: str | int,
    expires_delta: timedelta,
    token_type: str,
    extra_claims: dict[str | Any] | None = None
) -> str:
    now = datetime.now(UTC)

    payload: dict[str | Any] = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token():
    pass