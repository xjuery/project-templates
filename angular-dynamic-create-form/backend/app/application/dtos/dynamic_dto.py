"""
Builds Pydantic models at runtime from an ObjectTypeConfig.

Two model types are generated per config:
- CreateModel  : validates incoming POST payloads (no id field)
- ResponseModel: shapes the data returned by the API (includes id)
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, Literal, Optional, Tuple, Type, Union

from pydantic import BaseModel, EmailStr, Field, create_model

from app.domain.entities.field_config import FieldConfig, ObjectTypeConfig

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FIELD_PYTHON_TYPES: Dict[str, type] = {
    "text": str,
    "email": str,  # overridden to EmailStr below
    "number": float,
    "date": date,
    "boolean": bool,
    "select": str,
    "textarea": str,
}


def _base_type(field: FieldConfig) -> type:
    if field.type == "email":
        return EmailStr  # type: ignore[return-value]
    return _FIELD_PYTHON_TYPES.get(field.type, str)


def _select_literal(field: FieldConfig) -> type:
    """Return a Literal type built from the field's options values."""
    values = tuple(opt.value for opt in (field.options or []))
    if not values:
        return str
    # Literal[('a', 'b')] == Literal['a', 'b'] in Python's typing module
    return Literal[values]  # type: ignore[valid-type]


def _create_field_definition(
    field_cfg: FieldConfig,
    include_in_response: bool = False,
) -> Tuple[type, Any]:
    """Return a (annotation, FieldInfo) tuple for pydantic create_model()."""

    if field_cfg.type == "select" and field_cfg.options:
        python_type: type = _select_literal(field_cfg)
    else:
        python_type = _base_type(field_cfg)

    field_kwargs: Dict[str, Any] = {}

    # String constraints
    if field_cfg.type in ("text", "email", "textarea") or python_type is str:
        if field_cfg.min_length is not None:
            field_kwargs["min_length"] = field_cfg.min_length
        if field_cfg.max_length is not None:
            field_kwargs["max_length"] = field_cfg.max_length
        if field_cfg.pattern is not None:
            field_kwargs["pattern"] = field_cfg.pattern

    # Numeric constraints
    if field_cfg.type == "number":
        if field_cfg.min is not None:
            field_kwargs["ge"] = field_cfg.min
        if field_cfg.max is not None:
            field_kwargs["le"] = field_cfg.max

    if include_in_response:
        # Response fields are always optional (value may be null in DB)
        return (Optional[python_type], Field(default=None, **field_kwargs))

    if field_cfg.type == "boolean":
        # Booleans are never "required" – they always have a default
        default = field_cfg.default if field_cfg.default is not None else False
        return (bool, Field(default=default))

    if field_cfg.required:
        return (python_type, Field(..., **field_kwargs))

    # Optional field: use the config default if provided
    default = field_cfg.default if field_cfg.default is not None else None
    return (Optional[python_type], Field(default=default, **field_kwargs))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_create_model(config: ObjectTypeConfig) -> Type[BaseModel]:
    """Return a Pydantic model for validating POST payloads for *config*."""
    fields: Dict[str, Any] = {}
    for field_cfg in config.fields:
        fields[field_cfg.name] = _create_field_definition(field_cfg)
    model_name = f"Create{config.display_name}"
    return create_model(model_name, **fields)


def build_response_model(config: ObjectTypeConfig) -> Type[BaseModel]:
    """Return a Pydantic model for shaping GET/POST response bodies for *config*."""
    fields: Dict[str, Any] = {"id": (int, Field(...))}
    for field_cfg in config.fields:
        fields[field_cfg.name] = _create_field_definition(
            field_cfg, include_in_response=True
        )
    model_name = f"{config.display_name}Response"
    return create_model(model_name, **fields)
