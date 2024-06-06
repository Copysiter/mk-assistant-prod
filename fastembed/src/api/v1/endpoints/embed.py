from typing import Any, Iterable, List  # noqa

import numpy as np
import schemas
from api import deps
from core.config import settings
from fastapi import APIRouter, Depends, FastAPI, HTTPException  # noqa
from fastembed.embedding import TextEmbedding as Embedding
from utils import get_model_info, get_model_name, get_model_path

router = APIRouter()


@router.post("/", response_model=list[list[float]])
async def embed_query(
    embed: schemas.Embed, app: FastAPI = Depends(deps.get_app)
) -> Iterable[np.ndarray]:
    """
    Embeds a query using a specified model.

    Args:
        embed (Embed): The request object containing the model and query.

    Returns:
        dict[str, Iterable[np.ndarray]]: A dictionary containing the embedded query.

    Raises:it
        HTTPException: If there is an error in the request or embedding process.
    """
    provider = embed.provider
    model = embed.model
    query = embed.query

    try:
        if not hasattr(app, "embedding"):
            app.embedding = Embedding(
                get_model_name(provider, model),
                cache_dir=settings.CACHE_DIR,
                max_length=512,
                device="cpu",
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        embeddings = app.embedding.embed(query if isinstance(query, list) else [query])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return embeddings
