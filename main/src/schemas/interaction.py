from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class InteractionBase(BaseModel):
    ext_id: Optional[int] = None
    intent: Optional[str] = None
    subintent: Optional[str] = None
    query: Optional[str] = None
    modified_query: Optional[str] = None
    result: Optional[str] = None
    logic_chain: Optional[bool] = None


# Properties to receive via API on creation
class InteractionCreate(InteractionBase):
    ext_id: int
    intent: str
    query: str


# Properties to receive via API on update
class InteractionUpdate(InteractionBase):
    pass


class InteractionInDBBase(InteractionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class Interaction(InteractionInDBBase):
    pass


# Additional properties stored in DB
class InteractionInDB(InteractionInDBBase):
    pass


# List of users to return via API
class InteractionRows(BaseModel):
    data: List[Interaction]
    total: int
