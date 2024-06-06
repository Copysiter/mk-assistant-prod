from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class EventBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    channel_name: Optional[str] = None
    channel_url: Optional[str] = None


# Properties to receive via API on creation
class EventCreate(EventBase):
    name: str
    date: datetime


# Properties to receive via API on update
class EventUpdate(EventBase):
    pass


class EventInDBBase(EventBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Event(EventInDBBase):
    pass


# Additional properties stored in DB
class EventInDB(EventInDBBase):
    pass


# List of users to return via API
class EventRows(BaseModel):
    data: List[Event]
    total: int
