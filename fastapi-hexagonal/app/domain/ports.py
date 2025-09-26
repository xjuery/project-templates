from typing import Protocol, Iterable, Optional

from .entities import Item


class ItemRepository(Protocol):
    def add(self, item: Item) -> Item:
        ...

    def get(self, item_id: int) -> Optional[Item]:
        ...

    def list(self) -> Iterable[Item]:
        ...

    def remove(self, item_id: int) -> bool:
        ...


