"""
FastAPI application entry point.

Configures CORS (allowing the Angular dev server) and mounts all routers
under the /api prefix.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.exposition.routers.fields_router import router as fields_router
from app.exposition.routers.search_router import router as search_router

app = FastAPI(
    title="Employee Search API",
    description="FastAPI backend for the Angular Advanced Search template.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(fields_router, prefix="/api", tags=["Fields"])
app.include_router(search_router, prefix="/api", tags=["Search"])
