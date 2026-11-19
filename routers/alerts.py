from fastapi import APIRouter, HTTPException
from exceptions.handler import get_error_type
from dependency.all_dependencies import verified, db

alerts_router = APIRouter(prefix="/alerts")


# health check
@alerts_router.get("/health")
def health_check():
    return {"status": "OK"}


# register  a phone for push notifications
@alerts_router.put("/devices/register")
def register_phone(v: verified, db: db):
    try:
        pass
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# unregister a device
@alerts_router.delete("/devices/delete/{token}")
def unregister_device(v: verified, db: db, token: str):
    try:
        pass
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# set when to be notified
@alerts_router.put("/settings")
def set_notification_schedule(
    v: verified, db: db, budget_thresholds: list[int], bill_reminders_enabled: bool
):
    try:
        pass
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
