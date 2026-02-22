"""
Application Layer — Get Fields Use Case

Retrieves the list of searchable field definitions so the frontend can build
its dynamic filter UI. Orchestrates nothing beyond a single repository call.
"""

from app.domain.entities import FieldDefinition
from app.domain.ports.employee_repository import EmployeeRepository


class GetFieldsUseCase:
    def __init__(self, repository: EmployeeRepository) -> None:
        self._repository = repository

    def execute(self) -> list[FieldDefinition]:
        return self._repository.get_field_definitions()
