from fastapi import APIRouter

# from .endpoints import base, key, utils  # noqa
from .endpoints import base, key, role  # noqa

api_router = APIRouter()

api_router.include_router(base.router, prefix="", tags=["Info"])
api_router.include_router(key.router, prefix="/keys", tags=["Keys"])
api_router.include_router(role.router, prefix="/roles", tags=["Roles"])
