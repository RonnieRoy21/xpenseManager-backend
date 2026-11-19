from datetime import date

from fastapi import APIRouter, HTTPException
from dependency.all_dependencies import verified, db
from exceptions.handler import get_error_type

from models.goals import GoalsModel

goals_router = APIRouter(prefix="/goals")

# health check


@goals_router.get("/health")
def health_check():
    return {"status": "OK"}


# create a savings goal
@goals_router.post("/")
def create_goal(v: verified, db: db, goal: GoalsModel):
    try:
        goal.user_id = v.user_id
        return db.createGoal(g=goal)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# get all saved goals
@goals_router.get("/all")
def get_all_goals(
    v: verified,
    db: db,
):
    try:
        return db.getAllGoals(user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# add money to a goal
@goals_router.post("/contributions/{id}")
def contribute_to_goal(
    v: verified, db: db, id: int, amount: int, date: date = date.today()
):
    try:
        return db.contributeToGoal(
            g_id=id, user_id=v.user_id, amount=amount, update_date=date
        )
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# delete a goal
@goals_router.delete("/delete/{id}")
def delete_goal(v: verified, db: db, id: int):
    try:
        return db.deleteGoal(g_id=id, user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
