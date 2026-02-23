"""
Dependency injection wiring.

The repository singletons are created once at import time so that all
requests share the same in-memory store for the lifetime of the process.
"""

from app.domain.repositories.person_repository import PersonRepository
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.repositories.in_memory_person_repository import InMemoryPersonRepository
from app.infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository

_person_repository: PersonRepository = InMemoryPersonRepository()
_product_repository: ProductRepository = InMemoryProductRepository()


def get_person_repository() -> PersonRepository:
    return _person_repository


def get_product_repository() -> ProductRepository:
    return _product_repository
