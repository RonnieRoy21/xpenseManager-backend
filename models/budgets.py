from pydantic import BaseModel
import uuid
from datetime import date, datetime, timezone


class BudgetsModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    category_id: int
    limit_amount: int  # must be gt 0
    budget_month: date = date.today()
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
