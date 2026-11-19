from pydantic import BaseModel
from datetime import datetime, date, timezone
import uuid


class GoalsModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    name: str
    target_amount: int
    deadline: date
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    deleted_at: datetime | None
