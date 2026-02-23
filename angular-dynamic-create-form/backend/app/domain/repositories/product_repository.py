from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.product import Product


class ProductRepository(ABC):
    """Port (secondary) for product persistence."""

    @abstractmethod
    def find_all(self) -> List[Product]:
        """Return all stored products."""

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Return a product by its id, or None if not found."""

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Persist a new product and return it with its assigned id."""

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Delete a product by id. Return True if deleted, False if not found."""
