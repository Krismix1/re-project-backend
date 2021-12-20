"""Main module for API routes."""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()
ops_router = APIRouter()


@ops_router.get("/healthcheck", response_class=PlainTextResponse)
async def healthcheck() -> str:
    """Healthcheck endpoint."""
    return "OK"


@router.get("/hello")
async def hello_world():
    """Hello world endpoint."""
    return "Hello World"
