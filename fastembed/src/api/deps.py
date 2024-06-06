from fastapi import FastAPI, Request  # noqa


def get_app(request: Request) -> FastAPI:
    return request.app
