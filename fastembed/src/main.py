import uvicorn
from api.v1.api_router import api_router
from core.config import settings
from core.logger import LOGGING  # noqa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse


def init_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"{settings.API_VERSION_PREFIX}/docs",
        redoc_url=f"{settings.API_VERSION_PREFIX}/redoc",
        openapi_url=f"{settings.API_VERSION_PREFIX}/openapi.json",
        default_response_class=ORJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_VERSION_PREFIX)

    return app


app = init_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        workers=settings.UVICORN_WORKERS,
        log_config=LOGGING,
        access_log=True,
        reload=False,
    )
