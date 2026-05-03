from pydantic import BaseModel
from typing import List, Optional, Literal


class Node(BaseModel):
    id: int
    name: str
    type: Literal["folder", "activity"]
    parent_id: Optional[int]
    children: List["Node"] = []

Node.model_rebuild()