from functools import lru_cache

from app.application.use_cases import ItemService
from app.infrastructure.repositories import InMemoryItemRepository


@lru_cache
def get_item_service() -> ItemService:
    repository = InMemoryItemRepository()
    return ItemService(repository)


