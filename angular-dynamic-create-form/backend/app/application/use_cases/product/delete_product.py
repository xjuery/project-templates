from app.domain.repositories.product_repository import ProductRepository


class DeleteProduct:
    """Use case: delete a product by id."""

    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def execute(self, product_id: int) -> bool:
        """Return True if the product was deleted, False if not found."""
        return self._repository.delete(product_id)
