import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from app.config import settings
import jwt
from pwdlib import PasswordHash
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

password_hash = PasswordHash.recommended()

bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_token(
    subject: str | int,
    expires_delta: timedelta,
    token_type: str,
    extra_claims: dict[str, Any] | None = None
) -> str:

    now = datetime.now(UTC)

    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(
    subject: str | int,
    extra_claims: dict[str, Any] | None = None
) -> str:

    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return create_token(subject, expires, "access", extra_claims)


def create_refresh_token(
    subject: str | int,
    jti: str | None = None
) -> str:

    expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token_jti = jti or str(uuid.uuid4())

    return create_token(subject, expires, "refresh", {"jti": token_jti})


def decode_token(token: str, expected_type: str) -> dict[str, Any]:
    payload = jwt.decode(token, settings.SECRET_KEY,
                         algorithms=[settings.ALGORITHM])

    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError("Wrong token type")

    return payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_errors = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticete": "Bearer"}
    )

    try:
        payload = decode_token(credentials.credentials, "access")
        user_id = uuid.UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise credentials_errors

    user = db.get(User, user_id)

    if user is None:
        raise credentials_errors

    return user