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

    POSTGRES_SERVER: str = Field("localhost", env="POSTGRES_SERVER")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("postgres", env="POSTGRES_DB")

    POSTGRES_DSN: Optional[PostgresDsn] = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
        env="POSTGRES_DSN",
    )

    @field_validator("POSTGRES_DSN", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            port=values.data.get("POSTGRES_PORT"),
            path=f'{values.data.get("POSTGRES_DB") or ""}',
        )

    DATABASE_DELETE_ALL: bool = Field(False, env="DATABASE_DELETE_ALL")
    DATABASE_CREATE_ALL: bool = Field(True, env="DATABASE_CREATE_ALL")
    DATABASE_POOL_SIZE: int = Field(20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(40, env="DATABASE_MAX_OVERFLOW")

    FIRST_GLOBAL_ROLE: str = Field("global", env="FIRST_GLOBAL_ROLE")

    FIRST_API_KEY: str = Field(
        "568eD25b494fA9147416DfCd9Bbe71dFdC38F1c555F4c8b925f8c68C9EC17d5b",
        env="FIRST_API_KEY",
    )

    LOG_PATH: Union[str, None] = Field(None, env="LOG_PATH")
    LOG_FORMAT: str = Field(
        "%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s - %(message)s",
        env="LOG_DEFAULT_FORMAT",
    )
    LOG_LEVEL_DEFAULT: str = Field("INFO", env="LOG_LEVEL_DEFAULT")
    LOG_LEVEL_ACCESS: str = Field("INFO", env="LOG_LEVEL_ACCESS")
    LOG_LEVEL_SQLALCHEMY: str = Field("ERROR", env="LOG_LEVEL_SQLALCHEMY")

    SECRET_KEY: str = secrets.token_urlsafe(32)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
