from core.config import settings  # noqa
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root_handler():
    return {"version": f"v{settings.API_VERSION}"}
