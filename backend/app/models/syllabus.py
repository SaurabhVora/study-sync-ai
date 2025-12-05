from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class Topic(BaseModel):
    id: UUID
    name: str
    order_index: int
    keywords: Optional[List[str]] = []

class Unit(BaseModel):
    id: UUID
    name: str
    order_index: int
    topics: List[Topic] = []

class Subject(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    units: List[Unit] = []
