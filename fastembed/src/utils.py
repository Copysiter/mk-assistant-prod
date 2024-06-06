import os
from typing import Any

from core.config import settings
from fastapi import HTTPException
from fastembed.embedding import TextEmbedding as Embedding


def get_model_name(provider: str, model: str) -> str:
    return f"{provider}/{model}"


async def get_model_info(provider: str, model: str) -> dict[str, Any]:

    model_name = get_model_name(provider, model)
    models = Embedding.list_supported_models()
    models = list(filter(lambda x: x["model"] == model_name, models))

    if not models:
        return None

    return models[0]


async def get_model_path(provider: str, model: str) -> str:
    model_name = get_model_name(provider, model)
    model_info = await get_model_info(provider, model)

    if "hf" in model_info["sources"]:
        path_name = model_info["sources"]["hf"]
        path_name = path_name.split("/")
        path_name = f"models--{path_name[0]}--{path_name[1]}"
    elif "url" in model_info["sources"]:
        path_name = model_info["sources"]["url"]
        path_name = path_name.split("/")[-1]
        path_name = path_name.split(".")[0]
    else:
        raise ValueError(f"Model {model_name} doesn't exist.")

    path_name = os.path.join(os.getcwd(), settings.CACHE_DIR, path_name)

    if not os.path.exists(path_name):
        raise ValueError(f"Model {model_name} wasn't pulled.")

    return path_name
