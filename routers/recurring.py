from fastapi import APIRouter, HTTPException
from dependency.all_dependencies import verified, db
from exceptions.handler import get_error_type
from models.recurring_rules import RecurringRulesModel

recurring_router = APIRouter(prefix="/recurring-rules")


# health check
@recurring_router.get("/health")
def health_check():
    return {"status": "OK"}


# create a recurring rule
@recurring_router.post("/new")
def create_new_rule(v: verified, db: db, rule: RecurringRulesModel):
    try:
        rule.user_id = v.user_id
        return db.createRecurringRule(r=rule)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


@recurring_router.get("/all")
def get_all_rules(v: verified, db: db):
    try:
        return db.getAllRecurringRules(user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


@recurring_router.delete("/delete/{id}")
def delete_rule(v: verified, db: db, id: int):
    try:
        return db.deleteRecurringRule(user_id=v.user_id, r_id=id)

    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
