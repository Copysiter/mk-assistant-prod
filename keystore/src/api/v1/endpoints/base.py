from typing import Any, List  # noqa

import models  # noqa
import schemas
from api import deps  # noqa
from core.security import keygen  # noqa
from fastapi import APIRouter, Depends  # noqa

router = APIRouter()


@router.get("/", response_model=schemas.KeyPub)
async def key_info(key: models.Key = Depends(deps.get_active_key_info)) -> Any:
    """
    Get key info.
    """
    return key
