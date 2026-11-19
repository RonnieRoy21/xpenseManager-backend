from pydantic import BaseModel
from datetime import datetime, timezone
import uuid


class CategoriesModel(BaseModel):
    id: int | None
    user_id: uuid.UUID
    category_name: str
    category_type: str
    category_color: str = ""
    category_icon: str = ""
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
    deleted_at: datetime | None = None
