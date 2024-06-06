from fastapi import APIRouter

# from .endpoints import base, key, utils  # noqa
from .endpoints import base

api_router = APIRouter()

api_router.include_router(base.router, prefix="", tags=["Base"])
