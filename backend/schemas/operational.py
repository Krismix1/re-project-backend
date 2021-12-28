"""Schemas related to operational endpoints."""
from pydantic import BaseModel


class BuildInfo(BaseModel):
    """Information about the current running build."""

    build_id: str
