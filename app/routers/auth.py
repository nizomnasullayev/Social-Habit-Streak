from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead
from app.security import create_access_token
from app.services import auth

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserRead, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth.register(data, db)

@router.post("/login", response_model=TokenResponse, status_code=200)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = auth.authenticate(data.email, data.password, db)
    token = create_access_token(user.id)
    return TokenResponse(access_token=token)