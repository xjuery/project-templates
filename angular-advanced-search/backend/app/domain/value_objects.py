"""
Domain Layer — Value Objects

Immutable objects that represent domain concepts by their attributes rather
than by identity. They carry no side-effects and are safe to share.
"""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class SearchFilter:
    """
    A single filter predicate sent by the frontend.

    - field:    camelCase field name (e.g. 'isActive', 'createdAt')
    - operator: operator key (e.g. 'contains', 'greater_than', 'before')
    - value:    the comparison value (str, int, float, bool, or None for no-value operators)
    """

    id: str
    field: str
    operator: str
    value: Any = None


@dataclass(frozen=True)
class SearchQuery:
    """
    Complete, immutable description of a search request.

    Uses snake_case attribute names following Python conventions.
    The exposition layer maps the camelCase frontend payload to this object.
    """

    text: str = ""
    filters: tuple[SearchFilter, ...] = field(default_factory=tuple)
    combinator: Literal["and", "or"] = "and"
    page: int = 1
    page_size: int = 10
    sort_field: str = "id"
    sort_order: Literal["asc", "desc"] = "asc"


@dataclass(frozen=True)
class SearchResult:
    """
    Immutable result returned by the repository after applying a SearchQuery.

    data contains employee dicts (camelCase) ready for serialisation.
    """

    data: tuple[dict, ...]
    total: int
    page: int
    page_size: int
    total_pages: int
