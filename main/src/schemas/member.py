from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class MemberBase(BaseModel):
    ext_id: Optional[int] = None
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None
    company_country: Optional[str] = None
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    hobby: Optional[str] = None


# Properties to receive via API on creation
class MemberCreate(MemberBase):
    ext_id: int


# Properties to receive via API on update
class MemberUpdate(MemberBase):
    pass


class MemberInDBBase(MemberBase):
    id: int

    class Config:
        from_attributes = True


# Additional properties to return via API
class Member(MemberInDBBase):
    pass


# Additional properties stored in DB
class MemberInDB(MemberInDBBase):
    pass


# List of users to return via API
class MemberRows(BaseModel):
    data: List[Member]
    total: int
