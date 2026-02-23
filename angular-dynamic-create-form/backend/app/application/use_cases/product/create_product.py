from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class CreateProduct:
    """Use case: create and persist a new product."""

    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def execute(self, product: Product) -> Product:
        return self._repository.save(product)
