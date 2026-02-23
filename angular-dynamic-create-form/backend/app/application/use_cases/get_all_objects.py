from typing import Any, Dict, List

from app.domain.repositories.object_repository import ObjectRepository


class GetAllObjects:
    """Use case: retrieve all records for an object type."""

    def __init__(self, repository: ObjectRepository) -> None:
        self._repository = repository

    def execute(self) -> List[Dict[str, Any]]:
        return self._repository.find_all()
