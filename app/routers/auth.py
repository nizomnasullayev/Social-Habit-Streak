from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import RegisterRequest
from app.schemas.user import UserRead
from app.services import auth

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserRead, status_code=201)
def register_route(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth.register(data, db)