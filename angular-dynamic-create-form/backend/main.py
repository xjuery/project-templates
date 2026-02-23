from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing dependencies triggers the bootstrap sequence:
#   - JSON configs are loaded from domain/object_types/
#   - SQLAlchemy tables are registered
#   - SQLite schema is created
import app.exposition.dependencies  # noqa: F401

from app.exposition.routers.objects_router import router as objects_router

app = FastAPI(
    title="Dynamic Create Form API",
    description=(
        "FastAPI backend for the Angular Dynamic Create Form application. "
        "Built with Hexagonal Architecture. "
        "Object types and their fields are driven entirely by the JSON config "
        "files in app/domain/object_types/."
    ),
    version="2.0.0",
)

# ---------------------------------------------------------------------------
# CORS – allow the Angular dev server (port 4200) to call this API
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Fixed routes (must be registered before the dynamic /{resource} catch-all)
# ---------------------------------------------------------------------------

@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Dynamic object router  (registered last so fixed routes take priority)
# ---------------------------------------------------------------------------
app.include_router(objects_router)
