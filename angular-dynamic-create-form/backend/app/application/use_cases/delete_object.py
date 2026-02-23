from app.domain.repositories.object_repository import ObjectRepository


class DeleteObject:
    """Use case: delete a record by id for an object type."""

    def __init__(self, repository: ObjectRepository) -> None:
        self._repository = repository

    def execute(self, obj_id: int) -> bool:
        """Return True if the record was deleted, False if not found."""
        return self._repository.delete(obj_id)
