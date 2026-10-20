from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.security import (
    hash_password,
    verify_password
)
from app.schemas.auth import RegisterRequest
from fastapi import HTTPException

def register(data: RegisterRequest, db: Session) -> User:
    stmt = select(User).where(User.email == data.email.lower())
    existing_user = db.scalar(stmt)

    if existing_user:
        raise HTTPException(400, "Email already registered")
    
    hashed_password = hash_password(data.password)

    user = User(
        email = data.email,
        hashed_password = hashed_password,
        username = data.username,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate(email: str, password: str, db: Session) -> User:
    stmt = select(User).where(User.email == email.lower())
    user = db.scalar(stmt)
    
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")
    
    return user