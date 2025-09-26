from typing import Dict, Iterable, Optional

from app.domain.entities import Item
from app.domain.ports import ItemRepository


class InMemoryItemRepository(ItemRepository):
    def __init__(self) -> None:
        self._items: Dict[int, Item] = {}
        self._next_id: int = 1

    def add(self, item: Item) -> Item:
        item_id = self._next_id
        self._next_id += 1
        created = Item(id=item_id, name=item.name, description=item.description)
        self._items[item_id] = created
        return created

    def get(self, item_id: int) -> Optional[Item]:
        return self._items.get(item_id)

    def list(self) -> Iterable[Item]:
        return list(self._items.values())

    def remove(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None


