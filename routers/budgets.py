from fastapi import APIRouter, HTTPException
from exceptions.handler import get_error_type
from dependency.all_dependencies import verified, db
from models.budgets import BudgetsModel

budgets_router = APIRouter(prefix="/budgets")


@budgets_router.get("/health")
def health_check():
    return {"status": "OK"}


@budgets_router.post("/new")
def create_new_budgets(v: verified, db: db, budget: BudgetsModel):
    try:
        budget.user_id = v.user_id
        return db.createBudget(b=budget)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# get budget
@budgets_router.get("/all")
def get_all_budgets(v: verified, db: db):
    try:
        return db.getAllBudgets(user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# update  or create budget
@budgets_router.put("/new/{id}")
def edit_budget(v: verified, db: db, id: int, limit_amount: int, category_id: int):
    try:
        return db.updateBudget(
            b_id=id, user_id=v.user_id, c_id=category_id, amount=limit_amount
        )
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# delete budget
@budgets_router.delete("/delete/{id}")
def delete_budget(v: verified, db: db, id: int):
    try:
        return db.deleteBudget(user_id=v.user_id, b_id=id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
