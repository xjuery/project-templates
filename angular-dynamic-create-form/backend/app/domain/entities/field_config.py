from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class SelectOption:
    label: str
    value: Any


@dataclass
class FieldConfig:
    """Mirrors the FieldConfig TypeScript interface from the frontend."""

    name: str
    label: str
    type: str  # 'text' | 'email' | 'number' | 'date' | 'boolean' | 'select' | 'textarea'
    required: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min: Optional[float] = None
    max: Optional[float] = None
    pattern: Optional[str] = None
    default: Optional[Any] = None
    options: Optional[List[SelectOption]] = field(default=None)
    placeholder: Optional[str] = None
    hint: Optional[str] = None


@dataclass
class ObjectTypeConfig:
    """Mirrors the ObjectTypeConfig TypeScript interface from the frontend."""

    object_type: str    # e.g. "person"
    display_name: str   # e.g. "Person"
    api_endpoint: str   # e.g. "/api/persons"
    fields: List[FieldConfig] = field(default_factory=list)

    @property
    def resource(self) -> str:
        """The last path segment of api_endpoint (e.g. 'persons')."""
        return self.api_endpoint.rstrip("/").split("/")[-1]
