import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.check_in import CheckIn
from app.models.habit import Habit
from app.models.user import User
from app.services.habit import get_habit
from datetime import date
from fastapi import HTTPException

def check_in(db: Session, user: User, habit_id: uuid.UUID) -> CheckIn:
    habit = get_habit(db, user, habit_id)
    today = date.today()
    stmt = select(CheckIn).where(CheckIn.habit_id == habit.id, CheckIn.checked_on == today)
    existing_check_in = db.scalar(stmt)

    if existing_check_in:
        raise HTTPException(409, "Habit already checked in")
    
    create_check_in = CheckIn(
        habit_id = Habit.id,
        checked_on = today
    )

    db.add(create_check_in)
    db.commit()
    db.refresh(create_check_in)
    return create_check_in

def undo_check_in(db: Session, user: User, habit_id: uuid.UUID):
    remove_check_in = get_habit(db, user, habit_id)
    db.delete(remove_check_in)
    db.commit()

def calculate_streak(dates: list[date], today: date) -> int:
    is_clicked = False    