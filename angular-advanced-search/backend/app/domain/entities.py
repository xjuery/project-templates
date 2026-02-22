"""
Domain Layer — Entities

Core business objects representing the fundamental concepts of the domain.
These classes are pure Python with no framework dependencies.
"""

from dataclasses import dataclass


@dataclass
class FieldDefinition:
    """Describes a searchable field: its API key, display label, and data type."""

    field: str  # camelCase key used in API requests/responses
    label: str
    type: str   # 'string' | 'number' | 'date' | 'boolean'


@dataclass
class Employee:
    """
    Core entity representing an employee record.

    Attribute names follow Python conventions (snake_case).
    The to_dict() method produces the camelCase representation expected by the frontend.
    """

    id: int
    name: str
    email: str
    age: int
    salary: float
    score: float
    status: str
    department: str
    description: str
    is_active: bool
    is_verified: bool
    created_at: str
    updated_at: str
    birth_date: str

    def to_dict(self) -> dict:
        """Return a camelCase dict compatible with the frontend API contract."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "salary": self.salary,
            "score": self.score,
            "status": self.status,
            "department": self.department,
            "description": self.description,
            "isActive": self.is_active,
            "isVerified": self.is_verified,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "birthDate": self.birth_date,
        }
