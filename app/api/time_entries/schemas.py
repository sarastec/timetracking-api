from pydantic import BaseModel
from datetime import datetime

class TimerAction(BaseModel):
    activity_id: int
    time: datetime