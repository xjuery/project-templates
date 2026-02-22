"""
Exposition Layer — Dependency Injection

Wires use cases to their repository implementation using FastAPI's dependency
injection system. The repository is cached as a singleton so the in-memory
dataset is shared across all requests.
"""

from functools import lru_cache

from app.application.use_cases.export_csv import ExportCsvUseCase
from app.application.use_cases.get_fields import GetFieldsUseCase
from app.application.use_cases.search_employees import SearchEmployeesUseCase
from app.infrastructure.repositories.in_memory_employee_repository import (
    InMemoryEmployeeRepository,
)


@lru_cache(maxsize=1)
def _get_repository() -> InMemoryEmployeeRepository:
    """Singleton repository — the in-memory dataset lives here."""
    return InMemoryEmployeeRepository()


def get_fields_use_case() -> GetFieldsUseCase:
    return GetFieldsUseCase(_get_repository())


def get_search_use_case() -> SearchEmployeesUseCase:
    return SearchEmployeesUseCase(_get_repository())


def get_export_use_case() -> ExportCsvUseCase:
    return ExportCsvUseCase(_get_repository())
