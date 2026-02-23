from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.person import Person


class PersonRepository(ABC):
    """Port (secondary) for person persistence."""

    @abstractmethod
    def find_all(self) -> List[Person]:
        """Return all stored persons."""

    @abstractmethod
    def find_by_id(self, person_id: int) -> Optional[Person]:
        """Return a person by its id, or None if not found."""

    @abstractmethod
    def save(self, person: Person) -> Person:
        """Persist a new person and return it with its assigned id."""

    @abstractmethod
    def delete(self, person_id: int) -> bool:
        """Delete a person by id. Return True if deleted, False if not found."""
