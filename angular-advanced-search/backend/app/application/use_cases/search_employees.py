"""
Application Layer — Search Employees Use Case

Accepts a SearchQuery value object, delegates the filtering / sorting /
pagination to the repository, and returns a SearchResult.

All business-logic decisions about *what* to search live here; *how* to
store and retrieve data is the infrastructure's concern.
"""

from app.domain.ports.employee_repository import EmployeeRepository
from app.domain.value_objects import SearchQuery, SearchResult


class SearchEmployeesUseCase:
    def __init__(self, repository: EmployeeRepository) -> None:
        self._repository = repository

    def execute(self, query: SearchQuery) -> SearchResult:
        return self._repository.search(query)
