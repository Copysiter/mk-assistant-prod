from typing import Any, List  # noqa

import crud  # noqa
import models
import schemas
from api import deps  # noqa
from core.security import keygen  # noqa
from fastapi import APIRouter, Depends, HTTPException, status  # noqa
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=schemas.KeyRows)
async def read_keys(
    db: AsyncSession = Depends(deps.get_db),
    filters: List[schemas.Filter] = Depends(deps.request_filters),
    orders: List[schemas.Order] = Depends(deps.request_orders),
    skip: int = 0,
    limit: int = 100,
    _: models.Key = Depends(deps.get_global_key_info),
) -> Any:
    """
    Retrieve keys.
    """
    keys = await crud.key.get_rows(
        db, filters=filters, orders=orders, skip=skip, limit=limit
    )
    count = await crud.key.get_count(db, filters=filters)
    return {"data": jsonable_encoder(keys), "total": count}


@router.post("/")
async def generate_key(
    *,
    db: AsyncSession = Depends(deps.get_db),
    key_in: schemas.KeyCreate,
    _: models.Key = Depends(deps.get_global_key_info),
) -> Any:
    """
    Generate new key.
    """
    api_key = keygen.generate()
    key_in.hashed_key = keygen.hash(api_key)
    _ = await crud.key.create(db=db, obj_in=key_in)
    return {"api_key": api_key}


@router.put("/{id}", response_model=schemas.Key)
async def update_key(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    key_in: schemas.KeyUpdate,
    _: models.Key = Depends(deps.get_global_key_info),
) -> Any:
    """
    Update an key.
    """
    key = await crud.key.get(db=db, id=id)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Key not found"
        )
    key = await crud.key.update(db=db, db_obj=key, obj_in=key_in)
    return key


@router.get("/{id}", response_model=schemas.Key)
async def read_key(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    _: models.Key = Depends(deps.get_global_key_info),
) -> Any:
    """
    Get key by ID.
    """
    key = await crud.key.get(db=db, id=id)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Key not found"
        )
    return key


@router.delete("/{id}", response_model=schemas.Key)
async def delete_key(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    _: models.Key = Depends(deps.get_global_key_info),
) -> Any:
    """
    Delete an key.
    """
    key = await crud.key.get(db=db, id=id)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Key not found"
        )
    key = await crud.key.delete(db=db, id=id)
    return key
