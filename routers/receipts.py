from fastapi import APIRouter, HTTPException, UploadFile
from dependency.all_dependencies import verified, db
from exceptions.handler import get_error_type

receipts_router = APIRouter(prefix="/receipts")


@receipts_router.get("/health")
def health_check():
    return {"status": "OK"}


# get signed url to upload receipt image
@receipts_router.post("/upload")
async def get_signed_url(v: verified, db: db, transaction_id: int, image: UploadFile):
    try:
        response = await db.uploadReceipt(
            img=image, t_id=transaction_id, user_id=v.user_id
        )
        return response
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# get temporary url to view uploaded receipt
@receipts_router.get("/view/{transaction_id}")
def get_temporary_url(v: verified, db: db, transaction_id: int):
    try:
        return db.getReceiptUrl(t_id=transaction_id, user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
