from fastapi import APIRouter, HTTPException
from dependency.all_dependencies import verified, db
from exceptions.handler import get_error_type

analytics_router = APIRouter(prefix="/analytics")


@analytics_router.get("/health")
def health_check():
    return {"status": "OK"}


@analytics_router.get("/generate-report/{email}")
def generate_report_and_send_to_email(v: verified, db: db, email: str):
    try:
        pass
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
