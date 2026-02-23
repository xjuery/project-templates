"""
Builds SQLAlchemy Core Table objects from ObjectTypeConfig definitions.

Using SQLAlchemy Core (rather than SQLModel ORM models) allows us to create
tables dynamically at runtime without needing static Python class definitions.

The shared MetaData instance ensures that metadata.create_all(engine) creates
every registered table in a single call.
"""

from typing import Dict

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.engine import Engine

from app.domain.entities.field_config import FieldConfig, ObjectTypeConfig

metadata = MetaData()

# object_type → Table
_registry: Dict[str, Table] = {}


# ---------------------------------------------------------------------------
# Field → Column mapping
# ---------------------------------------------------------------------------

def _field_to_column(field: FieldConfig) -> Column:
    nullable = not field.required

    match field.type:
        case "text":
            return Column(field.name, String(field.max_length or 255), nullable=nullable)
        case "email":
            return Column(field.name, String(254), nullable=nullable)
        case "number":
            return Column(field.name, Float, nullable=nullable)
        case "date":
            return Column(field.name, Date, nullable=nullable)
        case "boolean":
            # Booleans are never truly required; they default server-side
            default = field.default if field.default is not None else False
            return Column(field.name, Boolean, default=default, nullable=True)
        case "select":
            return Column(field.name, String(100), nullable=nullable)
        case "textarea":
            return Column(field.name, Text, nullable=nullable)
        case _:
            return Column(field.name, String(255), nullable=nullable)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def register_table(config: ObjectTypeConfig) -> Table:
    """Create a Table from *config* and register it in the shared metadata."""
    columns = [Column("id", Integer, primary_key=True, autoincrement=True)]
    for field in config.fields:
        columns.append(_field_to_column(field))

    table = Table(config.object_type, metadata, *columns, extend_existing=True)
    _registry[config.object_type] = table
    return table


def get_table(object_type: str) -> Table:
    """Retrieve a previously registered table by object_type."""
    try:
        return _registry[object_type]
    except KeyError:
        raise KeyError(f"No table registered for object type '{object_type}'.")


def create_all_tables(engine: Engine) -> None:
    """Issue CREATE TABLE IF NOT EXISTS for every registered table."""
    metadata.create_all(engine)
