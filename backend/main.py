"""Main module for FastAPI with creation of the FastAPI app itself."""
import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.router import ops_router, router

OPEN_API_TAGS_METADATA = [
    {"name": "operational", "description": "Actions for DevOps."},
    {"name": "auth", "description": "Actions for authorization operations."},
]

logging.basicConfig(level=logging.INFO)


def request_validation_exception_handler(_request: Request, exc: RequestValidationError):
    logging.error("Invalid body %s", exc.json())
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


app = FastAPI(title="Internship platform API", version="0.1.0", openapi_tags=OPEN_API_TAGS_METADATA)

app.include_router(router, prefix="/api/v1")
app.include_router(ops_router)

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
