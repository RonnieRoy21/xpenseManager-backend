from fastapi import APIRouter, HTTPException
from exceptions.handler import get_error_type
from dependency.all_dependencies import verified, db

from datetime import date

insights_router = APIRouter(prefix="/insights")


# health check
@insights_router.get("/health")
def health_check():
    return {"status": "OK"}


# get insights
@insights_router.get("/")
def get_insights(v: verified, db: db, month: int = date.today().month):
    try:
        pass
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
