from fastapi import APIRouter

from .endpoints import embed, models

api_router = APIRouter()

api_router.include_router(models.router, prefix="/models", tags=["Models"])
api_router.include_router(embed.router, prefix="/embed", tags=["Embed"])
