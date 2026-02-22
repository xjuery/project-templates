"""
Exposition Layer — Pydantic Schemas

These classes are the HTTP-level contract (request bodies and response shapes).
They use camelCase field names to match the Angular frontend's API expectations.
The exposition layer translates between these schemas and domain value objects.
"""

from typing import Any, Literal

from pydantic import BaseModel


class FilterSchema(BaseModel):
    id: str
    field: str
    operator: str
    value: Any = None


class SearchQuerySchema(BaseModel):
    text: str = ""
    filters: list[FilterSchema] = []
    combinator: Literal["and", "or"] = "and"
    page: int = 1
    pageSize: int = 10
    sortField: str = "id"
    sortOrder: Literal["asc", "desc"] = "asc"


class FieldDefinitionSchema(BaseModel):
    field: str
    label: str
    type: str


class SearchResponseSchema(BaseModel):
    data: list[dict]
    total: int
    page: int
    pageSize: int
    totalPages: int
