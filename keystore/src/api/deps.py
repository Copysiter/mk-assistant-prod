from typing import Dict, List  # noqa

import crud  # noqa
import models
import schemas
from core.config import settings  # noqa
from core.security import keygen  # noqa
from db.session import async_session  # noqa
from fastapi import Depends, HTTPException, Request, Security, status  # noqa
from fastapi.security.api_key import APIKey, APIKeyHeader, APIKeyQuery  # noqa
from sqlalchemy.ext.asyncio import AsyncSession
from utils.query_string import parse  # noqa


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="X-Api-Key", auto_error=False)


def get_api_key(
    key_query: APIKey = Security(api_key_query),
    key_header: APIKey = Security(api_key_header),
) -> APIKey:
    if key_query:
        return key_query
    if key_header:
        return key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
    )


async def get_key_info(
    db: AsyncSession = Depends(get_db), key_in: APIKey = Security(get_api_key)
) -> models.Key:
    key = await crud.key.get_by_hash(db=db, hash=keygen.hash(key_in))
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
    if not (key.is_active and key.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive API key"
        )
    return key


async def get_active_key_info(
    key: models.Key = Depends(get_key_info),
) -> models.Key:
    if not key.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive role"
        )
    return key


async def get_global_key_info(
    key: models.Key = Depends(get_active_key_info),
) -> models.Key:
    if not key.role.is_global:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    return key


def check_permissions(
    permissions: List[str] = [],
    key: models.Key = Depends(get_key_info),
) -> bool:
    for permission in permissions:
        if permission not in key.role.permissions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
            )
    return True


def query_params(request: Request) -> Dict:
    params = parse(str(request.query_params), normalized=True)
    return params


def request_filters(params: Dict = Depends(query_params)) -> List | Dict:
    return params.get("filters", [])


def request_orders(params: Dict = Depends(query_params)) -> List:
    return params.get("orders", [])
