from pydantic import BaseModel
from typing import Optional

class ActivityEdit(BaseModel):
    name: str
    folder_id: Optional[int] = None
    