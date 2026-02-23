from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.field_config import ObjectTypeConfig


class ObjectConfigRepository(ABC):
    """Port (secondary) – loads object-type configurations."""

    @abstractmethod
    def find_all(self) -> List[ObjectTypeConfig]:
        """Return all available object-type configurations."""

    @abstractmethod
    def find_by_resource(self, resource: str) -> Optional[ObjectTypeConfig]:
        """Return the config whose apiEndpoint ends with /{resource}, or None."""

    @abstractmethod
    def find_by_object_type(self, object_type: str) -> Optional[ObjectTypeConfig]:
        """Return the config for a given objectType identifier, or None."""
