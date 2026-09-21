from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.auth.schemas import UserRegister, UserLogin
from app.database import get_db
from app.models.user import User
from app.auth.security import hash_password, verify_password, create_access_token



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

@router.post("/login")
def login(
    user_data: UserLogin,
    session: Session = Depends(get_db)
):
    user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if not user.hashed_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    password_is_valid = verify_password(
        user_data.password,
        user.hashed_password
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token({
        "sub": str(user.uid)
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }