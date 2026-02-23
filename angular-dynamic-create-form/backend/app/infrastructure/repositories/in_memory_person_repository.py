from threading import Lock
from typing import Dict, List, Optional

from app.domain.entities.person import Person
from app.domain.repositories.person_repository import PersonRepository


class InMemoryPersonRepository(PersonRepository):
    """Adapter (secondary) – stores persons in an in-memory dictionary.

    Thread-safe via a simple lock so the repository can be safely used
    even if the ASGI server runs multiple coroutines concurrently.
    """

    def __init__(self) -> None:
        self._store: Dict[int, Person] = {}
        self._next_id: int = 1
        self._lock = Lock()

    def find_all(self) -> List[Person]:
        with self._lock:
            return list(self._store.values())

    def find_by_id(self, person_id: int) -> Optional[Person]:
        with self._lock:
            return self._store.get(person_id)

    def save(self, person: Person) -> Person:
        with self._lock:
            person.id = self._next_id
            self._store[person.id] = person
            self._next_id += 1
            return person

    def delete(self, person_id: int) -> bool:
        with self._lock:
            if person_id not in self._store:
                return False
            del self._store[person_id]
            return True
