from pydantic import BaseModel
from datetime import datetime, timezone
import uuid


class DevicesModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    push_token: str
    platform: str  # either android or ios
    created_at: datetime = datetime.now(timezone.utc)
    last_seen_at: datetime = datetime.now(timezone.utc)
