"""
Adapter (secondary) – generic SQLite CRUD repository backed by a single
SQLAlchemy Core Table.

One instance of this class is created per object type (one per table).
"""

from datetime import date
from typing import Any, Dict, List, Optional

from sqlalchemy import Table
from sqlalchemy.engine import Engine

from app.domain.repositories.object_repository import ObjectRepository


class SQLiteObjectRepository(ObjectRepository):

    def __init__(self, engine: Engine, table: Table) -> None:
        self._engine = engine
        self._table = table

    # ------------------------------------------------------------------
    # ObjectRepository port
    # ------------------------------------------------------------------

    def find_all(self) -> List[Dict[str, Any]]:
        with self._engine.connect() as conn:
            rows = conn.execute(self._table.select()).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def find_by_id(self, obj_id: int) -> Optional[Dict[str, Any]]:
        with self._engine.connect() as conn:
            row = conn.execute(
                self._table.select().where(self._table.c.id == obj_id)
            ).fetchone()
        return self._row_to_dict(row) if row else None

    def save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        db_data = self._prepare_for_db(data)
        with self._engine.connect() as conn:
            result = conn.execute(self._table.insert().values(**db_data))
            conn.commit()
            new_id = result.inserted_primary_key[0]
        return {"id": new_id, **data}

    def delete(self, obj_id: int) -> bool:
        with self._engine.connect() as conn:
            result = conn.execute(
                self._table.delete().where(self._table.c.id == obj_id)
            )
            conn.commit()
        return result.rowcount > 0

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_dict(row: Any) -> Dict[str, Any]:
        """Convert a SQLAlchemy Row to a plain dict.

        date objects are converted to ISO strings so that the dict is
        fully JSON-serialisable even when FastAPI's jsonable_encoder is
        not in the call chain (e.g. in tests).
        """
        result: Dict[str, Any] = dict(row._mapping)
        for key, value in result.items():
            if isinstance(value, date):
                result[key] = value.isoformat()
        return result

    @staticmethod
    def _prepare_for_db(data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure Python objects are in a form SQLAlchemy Core accepts."""
        # SQLAlchemy handles date objects natively; nothing special needed.
        # We strip the id key if it was accidentally included.
        return {k: v for k, v in data.items() if k != "id"}
