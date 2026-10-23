import uuid
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.habit import Habit
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitUpdate


def get_habit(db: Session, user: User, habit_id: uuid.UUID) -> Habit:
    stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user.id)
    habit = db.scalar(stmt)

    if habit is None:
        raise HTTPException(404, "Habit not found")
    
    return habit

def create_habit(db: Session, user: User, data: HabitCreate) -> Habit:
    habit = Habit(
        user_id = user.id,
        name = data.name,
        description = data.description
    )

    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

def list_habits(db: Session, user: User) -> Habit:
    stmt = select(Habit).where(Habit.user_id == user.id).order_by(Habit.created_at.desc())
    return list(db.scalars(stmt).all())

def update_habit(db: Session, user: User, habit_id: uuid.UUID, data: HabitUpdate) -> Habit:
    habit = get_habit(db, user, habit_id)
    
    for key, value in data.model_dump(exclude_unset=True).items():
        if key in ("name", "is_archived") and value is None:
            continue
        setattr(habit, key, value)
        
    db.commit()
    db.refresh(habit)
    return habit

def delete_habit(db: Session, user: User, habit_id: uuid.UUID) -> Habit:
    habit = get_habit(db, user, habit_id)
    db.delete(habit)
    db.commit()