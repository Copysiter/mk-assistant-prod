from datetime import datetime
from typing import TYPE_CHECKING, List, Optional  # noqa

from pydantic import BaseModel, ConfigDict

from .role import Role, RoleBase


# Shared properties
class KeyBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    role_id: Optional[int] = None
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class KeyCreate(KeyBase):
    hashed_key: Optional[str] = None


# Properties to receive via API on update
class KeyUpdate(KeyBase):
    role_id: Optional[int] = None


class KeyInDBBase(KeyCreate):
    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Key(KeyInDBBase):
    role: Role


# Additional properties stored in DB
class KeyInDB(KeyInDBBase):
    pass


# Public properties
class KeyPub(KeyBase):
    role: RoleBase


# List of users to return via API
class KeyRows(BaseModel):
    data: List[Key]
    total: int
