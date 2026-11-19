from pydantic import BaseModel
from datetime import datetime, date
import uuid


class TransactionModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    transaction_date: date = date.today()
    transaction_amount: int
    category_id: int
    transaction_type: str  # can only be either "income" | "expense"
    transaction_note: str = ""
    transaction_receipt_url: str = ""
    transaction_source: str = "manual"  # can be "manual" | "mpesa" |"recurring"
    transaction_mpesa_code: str = ""
    recurring_rule_id: int | None = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
