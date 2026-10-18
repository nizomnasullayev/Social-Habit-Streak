import uuid
import jwt
from abc import ABC
from datetime import UTC, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.models.user import User
