from threading import Lock
from typing import Dict, List, Optional

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    """Adapter (secondary) – stores products in an in-memory dictionary.

    Thread-safe via a simple lock so the repository can be safely used
    even if the ASGI server runs multiple coroutines concurrently.
    """

    def __init__(self) -> None:
        self._store: Dict[int, Product] = {}
        self._next_id: int = 1
        self._lock = Lock()

    def find_all(self) -> List[Product]:
        with self._lock:
            return list(self._store.values())

    def find_by_id(self, product_id: int) -> Optional[Product]:
        with self._lock:
            return self._store.get(product_id)

    def save(self, product: Product) -> Product:
        with self._lock:
            product.id = self._next_id
            self._store[product.id] = product
            self._next_id += 1
            return product

    def delete(self, product_id: int) -> bool:
        with self._lock:
            if product_id not in self._store:
                return False
            del self._store[product_id]
            return True
