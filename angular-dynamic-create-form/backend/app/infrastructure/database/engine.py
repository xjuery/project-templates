"""
SQLite engine – created once and shared across the whole application.

SQLModel is used to create the engine so the rest of the infrastructure
stays consistent with the SQLModel / SQLAlchemy ecosystem.
The database file is created next to this module (backend/dynamic_form.db).
"""

from pathlib import Path

from sqlmodel import create_engine as sqlmodel_create_engine
from sqlalchemy.engine import Engine

_DB_PATH = Path(__file__).resolve().parent.parent.parent.parent / "dynamic_form.db"
_DATABASE_URL = f"sqlite:///{_DB_PATH}"

# check_same_thread=False is required for SQLite when used in a multi-threaded
# ASGI context (FastAPI / Starlette).
engine: Engine = sqlmodel_create_engine(
    _DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)
