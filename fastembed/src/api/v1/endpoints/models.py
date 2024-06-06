import shutil
from typing import Any, List  # noqa

from api import deps
from core.config import settings
from fastapi import HTTPException  # noqa
from fastapi import APIRouter, Depends, FastAPI, Request, Response
from fastembed.embedding import TextEmbedding as Embedding
from utils import get_model_info, get_model_name, get_model_path

router = APIRouter()


@router.get("/")
async def get_models() -> list[str]:
    """
    Retrieves a list of supported model names for embedding.

    Returns:
        A list of model names.
    """
    models = Embedding.list_supported_models()
    return [model["model"] for model in models]


@router.get("/{provider}/{model}")
async def get_model_info(provider: str, model: str) -> dict[str, Any]:
    """
    Retrieves information about a specific model from the provider.

    Args:
        provider (str): The provider of the model.
        model (str): The name of the model.

    Returns:
        dict[str, Any]: A dictionary containing information about the model.

    Raises:
        HTTPException: If the model is not found.
    """

    model_name = get_model_name(provider, model)
    model_info = get_model_info(provider, model)

    if not model_info:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found.")

    return model_info


@router.post("/pull/{provider}/{model}")
async def pull_model(
    provider: str, model: str, app: FastAPI = Depends(deps.get_app)
) -> dict[str, str]:
    """
    Pulls a model from the specified provider.

    Args:
        provider (str): The provider of the model.
        model (str): The name of the model.

    Returns:
        dict[str, str]: A dictionary containing a success message.

    Raises:
        HTTPException: If the model could not be pulled.
    """
    model_name = get_model_name(provider, model)
    try:
        app.embedding = Embedding(
            model_name, cache_dir=settings.CACHE_DIR, max_length=512
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Model {model_name} pulled successfully."}


@router.delete("/delete/{provider}/{model}")
async def delete_model(
    provider: str, model: str, app: FastAPI = Depends(deps.get_app)
) -> dict[str, str]:
    """
    Deletes a model from the specified provider.

    Args:
        provider (str): The provider of the model.
        model (str): The name of the model to delete.

    Returns:
        dict[str, str]: A dictionary containing a success message.

    Raises:
        HTTPException: If the model could not be deleted (e.g. if it doesn't exist or wasn't pulled)
    """
    model_name = get_model_name(provider, model)

    try:
        path_name = await get_model_path(provider, model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    shutil.rmtree(path_name)
    delattr(app, "embedding")

    return {"message": f"Model {model_name} deleted successfully."}
