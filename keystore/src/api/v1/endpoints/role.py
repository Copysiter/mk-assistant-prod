from typing import Any, List  # noqa

import crud  # noqa
import models
import schemas
from api import deps  # noqa
from fastapi import APIRouter, Depends, HTTPException, status  # noqa
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=schemas.RoleRows)
async def read_roles(
    db: AsyncSession = Depends(deps.get_db),
    filters: List[schemas.Filter] = Depends(deps.request_filters),
    orders: List[schemas.Order] = Depends(deps.request_orders),
    skip: int = 0,
    limit: int = 100,
    _: models.Key = Depends(deps.get_global_key_info),
) -> Any:
    """
    Retrieve roles.
    """
    roles = await crud.role.get_rows(
        db, filters=filters, orders=orders, skip=skip, limit=limit
    )
    count = await crud.role.get_count(db, filters=filters)
    return {"data": jsonable_encoder(roles), "total": count}


@router.post("/", response_model=schemas.Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
    _: models.Key = Depends(deps.get_global_key_info)
) -> Any:
    """
    Create new role.
    """
    role = await crud.role.create(db=db, obj_in=role_in)
    return role


@router.put("/{id}", response_model=schemas.Role)
async def update_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    role_in: schemas.RoleUpdate,
    _: models.Key = Depends(deps.get_global_key_info)
) -> Any:
    """
    Update an role.
    """
    role = await crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    role = await crud.role.update(db=db, db_obj=role, obj_in=role_in)
    return role


@router.get("/{id}", response_model=schemas.Role)
async def read_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    _: models.Key = Depends(deps.get_global_key_info)
) -> Any:
    """
    Get role by ID.
    """
    role = await crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return role


@router.delete("/{id}", response_model=schemas.Role)
async def delete_role(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    _: models.Key = Depends(deps.get_global_key_info)
) -> Any:
    """
    Delete an role.
    """
    role = await crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    role = await crud.role.delete(db=db, id=id)
    return role
