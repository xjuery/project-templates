"""
Dependency injection wiring.

At import time this module:
  1. Loads all object-type configs from the domain JSON files.
  2. Registers a SQLAlchemy table for each config.
  3. Creates the SQLite schema (CREATE TABLE IF NOT EXISTS).
  4. Instantiates one SQLiteObjectRepository per object type.

FastAPI route handlers obtain what they need through the functions at the
bottom of this file.
"""

from typing import Dict

from app.domain.repositories.object_config_repository import ObjectConfigRepository
from app.domain.repositories.object_repository import ObjectRepository
from app.infrastructure.config.file_object_config_repository import (
    FileObjectConfigRepository,
)
from app.infrastructure.database.engine import engine
from app.infrastructure.database.table_registry import (
    create_all_tables,
    get_table,
    register_table,
)
from app.infrastructure.repositories.sqlite_object_repository import (
    SQLiteObjectRepository,
)

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

# 1. Config repository (reads JSON files from domain/object_types/)
_config_repo: ObjectConfigRepository = FileObjectConfigRepository()

# 2. Register one SQLAlchemy table per config and collect them
for _cfg in _config_repo.find_all():
    register_table(_cfg)

# 3. Create the SQLite schema (idempotent – uses CREATE TABLE IF NOT EXISTS)
create_all_tables(engine)

# 4. One object repository per object_type
_object_repos: Dict[str, ObjectRepository] = {
    _cfg.object_type: SQLiteObjectRepository(
        engine=engine,
        table=get_table(_cfg.object_type),
    )
    for _cfg in _config_repo.find_all()
}


# ---------------------------------------------------------------------------
# FastAPI dependency functions
# ---------------------------------------------------------------------------

def get_config_repository() -> ObjectConfigRepository:
    return _config_repo


def get_object_repository(object_type: str) -> ObjectRepository:
    """Return the repository for *object_type*, raising KeyError if unknown."""
    repo = _object_repos.get(object_type)
    if repo is None:
        raise KeyError(f"No repository found for object_type='{object_type}'.")
    return repo
