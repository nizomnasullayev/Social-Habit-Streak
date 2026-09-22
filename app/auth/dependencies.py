from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.config import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models.user import User


security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: Session = Depends(get_db)
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        user_uid: str | None = payload.get("sub")

        if user_uid is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
        
    user = session.exec(
        select(User).where(User.uid == user_uid)
    ).first()

    if user is None:
        raise credentials_exception
    
    return user