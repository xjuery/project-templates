from app.domain.repositories.person_repository import PersonRepository


class DeletePerson:
    """Use case: delete a person by id."""

    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    def execute(self, person_id: int) -> bool:
        """Return True if the person was deleted, False if not found."""
        return self._repository.delete(person_id)
