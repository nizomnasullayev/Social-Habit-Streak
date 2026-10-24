import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.check_in import CheckIn
from app.models.user import User
from app.services.habit import get_habit
from datetime import date
from fastapi import HTTPException

def check_in(db: Session, user: User, habit_id: uuid.UUID) -> CheckIn:
    habit = get_habit(db, user, habit_id)
    today = date.today()

    if habit.is_archived:
        raise HTTPException(400, "Cannot check in on an archived habit")

    stmt = select(CheckIn).where(CheckIn.habit_id == habit.id, CheckIn.checked_on == today)
    existing_check_in = db.scalar(stmt)

    if existing_check_in:
        raise HTTPException(409, "Habit already checked in")
    
    create_check_in = CheckIn(
        habit_id = habit.id,
        checked_on = today
    )

    db.add(create_check_in)
    db.commit()
    db.refresh(create_check_in)
    return create_check_in

def undo_check_in(db: Session, user: User, habit_id: uuid.UUID):
    habit = get_habit(db, user, habit_id)
    today = date.today()
    stmt = select(CheckIn).where(CheckIn.habit_id == habit.id, CheckIn.checked_on == today)
    remove = db.scalar(stmt)

    if remove is None:
        raise HTTPException(404, "Check-in not found")

    db.delete(remove)
    db.commit()