"""Main module for FastAPI with creation of the FastAPI app itself."""
from fastapi import FastAPI

from backend.db import models
from backend.db.database import engine
from backend.router import ops_router, router

models.Base.metadata.create_all(bind=engine)

OPEN_API_TAGS_METADATA = [
    {"name": "auth", "description": "Actions for authorization operations."},
]


app = FastAPI(title="Internship platform API", version="0.1.0", openapi_tags=OPEN_API_TAGS_METADATA)

app.include_router(router, prefix="/api/v1")
app.include_router(ops_router)
