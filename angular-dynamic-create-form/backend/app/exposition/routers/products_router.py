from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.product_dto import CreateProductDTO, ProductResponseDTO
from app.application.use_cases.product.create_product import CreateProduct
from app.application.use_cases.product.delete_product import DeleteProduct
from app.application.use_cases.product.get_all_products import GetAllProducts
from app.exposition.dependencies import get_product_repository
from app.domain.repositories.product_repository import ProductRepository

router = APIRouter(prefix="/products", tags=["products"])


def _get_all_products_uc(repo: ProductRepository = Depends(get_product_repository)) -> GetAllProducts:
    return GetAllProducts(repo)


def _create_product_uc(repo: ProductRepository = Depends(get_product_repository)) -> CreateProduct:
    return CreateProduct(repo)


def _delete_product_uc(repo: ProductRepository = Depends(get_product_repository)) -> DeleteProduct:
    return DeleteProduct(repo)


@router.get("", response_model=List[ProductResponseDTO], status_code=status.HTTP_200_OK)
def list_products(use_case: GetAllProducts = Depends(_get_all_products_uc)) -> List[ProductResponseDTO]:
    """Return all products."""
    products = use_case.execute()
    return [ProductResponseDTO.from_entity(p) for p in products]


@router.post("", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: CreateProductDTO,
    use_case: CreateProduct = Depends(_create_product_uc),
) -> ProductResponseDTO:
    """Create a new product."""
    product = use_case.execute(payload.to_entity())
    return ProductResponseDTO.from_entity(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    use_case: DeleteProduct = Depends(_delete_product_uc),
) -> None:
    """Delete a product by id."""
    deleted = use_case.execute(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )
