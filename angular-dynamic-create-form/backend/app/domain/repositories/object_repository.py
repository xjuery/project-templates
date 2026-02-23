from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ObjectRepository(ABC):
    """Port (secondary) – generic CRUD for a single object type.

    All records are represented as plain dicts so the repository stays
    independent of any specific entity class.
    """

    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]]:
        """Return all stored records."""

    @abstractmethod
    def find_by_id(self, obj_id: int) -> Optional[Dict[str, Any]]:
        """Return a record by id, or None if not found."""

    @abstractmethod
    def save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Persist a new record and return it with its assigned id."""

    @abstractmethod
    def delete(self, obj_id: int) -> bool:
        """Delete a record by id. Return True if deleted, False if not found."""
