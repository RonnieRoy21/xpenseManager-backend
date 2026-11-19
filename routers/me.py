from fastapi import APIRouter, HTTPException
from exceptions.handler import get_error_type

from models.profiles import ProfilesModel
from dependency.all_dependencies import db, verified

me_router = APIRouter(prefix="/me")


# login
@me_router.post("/login")
def sign_in(email: str, paswd: str, db: db):
    try:
        return db.loginUser(email=email, passwd=paswd)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# sign up
@me_router.post("/signUp")
def create_user(details: ProfilesModel, pswd: str, db: db):
    try:
        res = db.signUpUSer(email=details.email, passwd=pswd, name=details.name)
        if res == True:
            return {
                "message": "Account created",
            }

    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# fetch my profile
@me_router.get("/profile")
def get_profile(v: verified):
    try:
        return v
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
