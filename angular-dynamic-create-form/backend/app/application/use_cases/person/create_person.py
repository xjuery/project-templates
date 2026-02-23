from app.domain.entities.person import Person
from app.domain.repositories.person_repository import PersonRepository


class CreatePerson:
    """Use case: create and persist a new person."""

    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    def execute(self, person: Person) -> Person:
        return self._repository.save(person)
