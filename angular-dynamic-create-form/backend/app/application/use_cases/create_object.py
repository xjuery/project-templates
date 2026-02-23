from typing import Any, Dict

from app.domain.repositories.object_repository import ObjectRepository


class CreateObject:
    """Use case: persist a new record for an object type."""

    def __init__(self, repository: ObjectRepository) -> None:
        self._repository = repository

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._repository.save(data)
