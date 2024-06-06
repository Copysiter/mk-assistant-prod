from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class PlaceBase(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    referer: Optional[str] = None
    comment: Optional[str] = None


# Properties to receive via API on creation
class PlaceCreate(PlaceBase):
    name: str
    contacts: str


# Properties to receive via API on update
class PlaceUpdate(PlaceBase):
    pass


class PlaceInDBBase(PlaceBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Place(PlaceInDBBase):
    pass


# Additional properties stored in DB
class PlaceInDB(PlaceInDBBase):
    pass


# List of users to return via API
class PlaceRows(BaseModel):
    data: List[Place]
    total: int
