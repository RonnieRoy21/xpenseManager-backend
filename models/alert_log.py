from pydantic import BaseModel
from datetime import datetime, timezone
import uuid


class AlertLogModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    budget_id: int
    threshold: int
    sent_at: datetime = datetime.now(timezone.utc)
