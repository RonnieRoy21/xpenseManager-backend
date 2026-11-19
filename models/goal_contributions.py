from pydantic import BaseModel
from datetime import date, datetime, timezone
import uuid


class GoalContributionModel(BaseModel):
    id: int | None
    date: date = date.today()
    user_id: uuid.UUID
    goal_id: int
    amount: int
    created_at: datetime = datetime.now(timezone.utc)
