from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.exposition.routers.persons_router import router as persons_router
from app.exposition.routers.products_router import router as products_router

app = FastAPI(
    title="Dynamic Create Form API",
    description=(
        "FastAPI backend for the Angular Dynamic Create Form application. "
        "Built with Hexagonal Architecture."
    ),
    version="1.0.0",
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
# Routers
# ---------------------------------------------------------------------------
app.include_router(persons_router)
app.include_router(products_router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
