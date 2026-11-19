from fastapi import APIRouter, HTTPException
from exceptions.handler import get_error_type
from dependency.all_dependencies import verified, db

from models.mpesa_drafts import MpesaDraftModel

mpesa_router = APIRouter(prefix="/mpesa/drafts")


# health check
@mpesa_router.get("/health")
def health_check():
    return {"status": "OK"}


# submit a draft
@mpesa_router.post("/submit")
def submit_draft(v: verified, db: db, draft: MpesaDraftModel):
    try:
        draft.user_id = v.user_id
        return db.createDraft(d=draft)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# retrieve  drafts awaiting confirmation
@mpesa_router.get("/all")
def fetch_all_drafts(
    v: verified,
    db: db,
):
    try:
        return db.getAllDrafts(user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# confirm a draft to become a transaction
@mpesa_router.post("/confirm/{id}")
def confirm_draft(v: verified, db: db, id: int, category_id: int, note: str | None):
    try:
        return db.confirmPendingDraft(d_id=id, user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# delete draft
@mpesa_router.delete("/delete/{id}")
def delete_draft(v: verified, db: db, id: int):
    try:
        return db.deleteDraft(d_id=id, user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
