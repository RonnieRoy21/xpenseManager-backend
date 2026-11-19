from pydantic import BaseModel
from datetime import datetime, timezone
import uuid


class MpesaDraftModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    mpesa_code: str
    amount: int
    direction: str  # must be either "sent" | "received"
    counterparty: str
    occurred_at: str
    transaction_id: int
    status: str = "pending"  # can be "pending" | "confirmed" | "discarded"
    suggested_category_id: int
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
