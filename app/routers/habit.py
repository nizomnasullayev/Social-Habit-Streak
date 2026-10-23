import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.security import get_current_user
from app.services import habit as habit_service

router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)

@router.post("", response_model=HabitRead, status_code=201)
def create_habit(data: HabitCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return habit_service.create_habit(db, current_user, data)

@router.get("", response_model=list[HabitRead])
def list_habits(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return habit_service.list_habits(db, current_user)

@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return habit_service.get_habit(db, current_user, habit_id)

@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(habit_id: uuid.UUID, data: HabitUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return habit_service.update_habit(db, current_user, habit_id, data)

@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    habit_service.delete_habit(db, current_user, habit_id)