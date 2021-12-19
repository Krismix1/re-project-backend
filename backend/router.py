"""Main module for API routes."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def hello_world():
    """Hello world endpoint."""
    return "Hello World"
