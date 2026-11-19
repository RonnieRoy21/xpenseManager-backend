from pydantic import BaseModel
from datetime import datetime, timezone
import uuid


class AlertSettingsModel(BaseModel):
    user_id: uuid.UUID
    bill_reminders_enabled: bool
    updated_at: datetime = datetime.now(timezone.utc)
    budget_thresholds: list[int]
