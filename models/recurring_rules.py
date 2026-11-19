from pydantic import BaseModel
from datetime import datetime, timezone, date
import uuid


class RecurringRulesModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    category_id: int
    rule_type: str  # either "income" or  "expense"
    amount: int
    note: str = ""
    frequency: str  # either "daily" | "weekly " | "monthly"
    start_date: datetime
    end_date: datetime | None  # has to be ge start date
    next_run_date: date  # calculate from frequency
    active: bool = True
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
