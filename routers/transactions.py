from datetime import date

from fastapi import APIRouter, HTTPException, Depends
from exceptions.handler import get_error_type
from dependency.all_dependencies import verified, db
from models.transactions import TransactionModel

transaction_router = APIRouter(
    prefix="/transactions",
)


# health check
@transaction_router.get("/health")
def health_check():
    return {"status": "OK"}


# create new transaction and return it
@transaction_router.post("/new")
def post_transaction(v: verified, db: db, transaction: TransactionModel):
    try:
        if not transaction:
            raise ValueError

        transaction.user_id = v.user_id
        return db.addTransaction(t=transaction)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# get all transactions
@transaction_router.get("/all")
def get_all_transactions(
    v: verified,
    db: db,
):
    try:
        return db.getAllTransactions(user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# get specific transaction
@transaction_router.get("/one/{id}")
def get_specific_transaction(v: verified, db: db, id: int):
    try:
        return db.getsingleTransaction(t_id=id, user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# edit sepcific transaction
@transaction_router.patch("/edit/{id}")
def edit_one_transaction(
    v: verified,
    db: db,
    id: int,
    category_id: int,
    amount: int | None = None,
    type: str | None = None,
    date: date | None = None,
    note: str | None = None,
):
    try:
        return db.editTransaction(
            t_id=id,
            user_id=v.user_id,
            amt=amount,
            date=date,
            c_id=category_id,
            note=note,
            t_type=type,
        )
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# delete specific transaction
@transaction_router.delete("/delete/{id}")
def delete_transaction(v: verified, db: db, id: int):
    try:
        return db.deleteTransaction(t_id=id, user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
