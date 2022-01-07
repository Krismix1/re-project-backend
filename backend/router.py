"""Main module for API routes."""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from backend.core.config import SETTINGS
from backend.routers import auth
from backend.schemas.operational import BuildInfo

router = APIRouter()
ops_router = APIRouter()
router.include_router(auth.router)


@ops_router.get("/healthcheck", response_class=PlainTextResponse, tags=["operational"])
async def healthcheck() -> str:
    """Heroku healthcheck endpoint."""
    return "OK"


@ops_router.get("/build-info", response_model=BuildInfo, tags=["operational"])
async def build_info():
    return {"build_id": SETTINGS.BUILD_ID}
