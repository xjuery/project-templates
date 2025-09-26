from typing import Iterable, Optional

from app.domain.entities import Item
from app.domain.ports import ItemRepository


class ItemService:
    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def create_item(self, name: str, description: Optional[str]) -> Item:
        item = Item(id=None, name=name, description=description)
        created = self._repository.add(item)
        return created

    def get_item(self, item_id: int) -> Optional[Item]:
        return self._repository.get(item_id)

    def list_items(self) -> Iterable[Item]:
        return self._repository.list()

    def delete_item(self, item_id: int) -> bool:
        return self._repository.remove(item_id)


