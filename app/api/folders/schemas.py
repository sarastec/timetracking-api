from pydantic import BaseModel
from typing import Optional

class FolderEdit(BaseModel):
    name: str
    parent_id: Optional[int] = None
    