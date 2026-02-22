"""
Domain Layer — Repository Port (outbound port)

This abstract base class is the contract that the Application Layer relies on.
The Infrastructure Layer provides the concrete implementation.
Following Hexagonal Architecture, the domain defines the interface; frameworks
and storage details are pushed outward into adapters.
"""

from abc import ABC, abstractmethod

from app.domain.entities import Employee, FieldDefinition
from app.domain.value_objects import SearchQuery, SearchResult


class EmployeeRepository(ABC):
    """
    Outbound port: defines every storage operation the application needs.
    Concrete implementations live in app.infrastructure.repositories.
    """

    @abstractmethod
    def get_field_definitions(self) -> list[FieldDefinition]:
        """Return the ordered list of searchable field definitions."""
        ...

    @abstractmethod
    def search(self, query: SearchQuery) -> SearchResult:
        """
        Execute a full search: text filter, attribute filters, sort, and
        pagination. Returns a paginated SearchResult.
        """
        ...

    @abstractmethod
    def get_all_matching(self, query: SearchQuery) -> list[Employee]:
        """
        Return every employee that matches the query without pagination.
        Used by the CSV export use-case.
        """
        ...
