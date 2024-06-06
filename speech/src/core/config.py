import secrets
from typing import Any, Dict, List, Optional, Union  # noqa

from pydantic import (Field, PostgresDsn, ValidationInfo,  # noqa
                      field_validator)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("FastAPI", env="PROJECT_NAME")
    API_VERSION: str = Field("1", env="API_VERSION")
    API_VERSION_PREFIX: str = Field("/api/v1", env="API_VERSION_PREFIX")

    UVICORN_HOST: str = Field("127.0.0.1", env="UVICORN_HOST")
    UVICORN_PORT: int = Field(8000, env="UVICORN_PORT")
    UVICORN_WORKERS: int = Field(1, env="UVICORN_WORKERS")

    BACKEND_CORS_ORIGINS: Union[str, List[str]] = Field("*", env="BACKEND_CORS_ORIGINS")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    LOG_PATH: Union[str, None] = Field(None, env="LOG_PATH")
    LOG_FORMAT: str = Field(
        "%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s - %(message)s",
        env="LOG_DEFAULT_FORMAT",
    )
    LOG_LEVEL_DEFAULT: str = Field("INFO", env="LOG_LEVEL_DEFAULT")
    LOG_LEVEL_ACCESS: str = Field("INFO", env="LOG_LEVEL_ACCESS")
    LOG_LEVEL_SQLALCHEMY: str = Field("ERROR", env="LOG_LEVEL_SQLALCHEMY")

    ELEVENLABS_API_KEY: str = Field(None, env="ELEVENLABS_API_KEY")
    ELEVENLABS_MODEL: str = Field("eleven_multilingual_v2", env="ELEVENLABS_MODEL")
    ELEVENLABS_VOICE_ID: str = Field("WczBIOau2qV9z7nLeDqq", env="ELEVENLABS_VOICE_ID")

    SBER_SPEECH_TOKEN: str = Field(None, env="SBER_SPEECH_TOKEN")
    SBER_SPEECH_API_VERSION: str = Field(
        "SALUTE_SPEECH_PERS", env="SBER_SPEECH_API_VERSION"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
