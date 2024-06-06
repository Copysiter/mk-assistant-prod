from typing import List, Optional  # noqa

from pydantic import BaseModel, ConfigDict


# Shared properties
class RoleBase(BaseModel):
    name: str = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = []
    is_active: Optional[bool] = True
    is_global: Optional[bool] = True


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    name: Optional[int] = None


class RoleInDBBase(RoleBase):
    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Role(RoleInDBBase):
    pass


# Additional properties stored in DB
class RoleInDB(RoleInDBBase):
    pass


# List of users to return via API
class RoleRows(BaseModel):
    data: List[Role]
    total: int
