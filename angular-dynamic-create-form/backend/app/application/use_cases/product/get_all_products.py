from typing import List

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class GetAllProducts:
    """Use case: retrieve all products."""

    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def execute(self) -> List[Product]:
        return self._repository.find_all()
