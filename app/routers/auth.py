from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.auth.schemas import UserRegister
from app.database import get_db
from app.models.user import User
from app.auth.security import hash_password



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(
    user_data: UserRegister,
    session: Session = Depends(get_db)
):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user_data.password)

    user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.uid
    }