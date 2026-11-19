from pydantic import BaseModel
import uuid
from datetime import datetime
from datetime import timezone as tz


class ProfilesModel(BaseModel):
    user_id: uuid.UUID  # supabase will generate one when creating a user
    name: str
    currency: str = "KES"
    timezone: str = "Africa/Nairobi"
    created_at: datetime = datetime.now(tz.utc)
    email: str
