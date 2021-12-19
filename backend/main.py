"""Main module for FastAPI with creation of the FastAPI app itself."""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from backend.router import router

OPEN_API_TAGS_METADATA = [
    {"name": "auth", "description": "Actions for authorization operations."},
]


app = FastAPI(title="Internship platform API")

app.include_router(router, prefix="/api/v1")


def custom_openapi():
    """Custom OpenAPI wrapper as seen in FastAPI docs.

    See: https://fastapi.tiangolo.com/advanced/extending-openapi/
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="0.1.0",
        routes=app.routes,
        tags=OPEN_API_TAGS_METADATA,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
