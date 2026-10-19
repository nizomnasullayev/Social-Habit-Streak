import uuid
import jwt
from abc import ABC
from datetime import UTC, datetime, timedelta
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.models.user import User
from app.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password
)
from app.schemas.auth import LoginRequest, RegisterRequest


async def register(db) -> User:
    pass

async def login() -> User:
    pass