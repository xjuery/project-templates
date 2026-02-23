from typing import List

from app.domain.entities.person import Person
from app.domain.repositories.person_repository import PersonRepository


class GetAllPersons:
    """Use case: retrieve all persons."""

    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    def execute(self) -> List[Person]:
        return self._repository.find_all()
