from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.habit import Habit
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead


router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)

@router.post("/", response_model=HabitRead)
def create_habit(
    habit_data: HabitCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    habit = Habit(
        user_uid=current_user.uid,
        name=habit_data.name,
        frequency=habit_data.frequency
    )

    session.add(habit)
    session.commit()
    session.refresh(habit)

    return habit

@router.get("/", response_model=list[HabitRead])
def get_my_habits(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    habits = session.exec(
        select(Habit).where(
            Habit.user_uid == current_user.uid
        )
    ).all()

    return habits