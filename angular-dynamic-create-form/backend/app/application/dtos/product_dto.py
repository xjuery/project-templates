import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.domain.entities.product import Product, ProductCategory

_SKU_PATTERN = re.compile(r"^[A-Z0-9-]+$")


class CreateProductDTO(BaseModel):
    """Inbound DTO – validated data coming from the API request."""

    name: str = Field(..., min_length=2, max_length=100)
    sku: str
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    category: ProductCategory
    description: Optional[str] = Field(default=None, max_length=1000)
    releaseDate: Optional[date] = None
    inStock: bool = True

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: str) -> str:
        if not _SKU_PATTERN.match(value):
            raise ValueError("SKU must match pattern ^[A-Z0-9-]+$")
        return value

    def to_entity(self) -> Product:
        return Product(
            name=self.name,
            sku=self.sku,
            price=self.price,
            quantity=self.quantity,
            category=self.category,
            description=self.description,
            release_date=self.releaseDate,
            in_stock=self.inStock,
        )


class ProductResponseDTO(BaseModel):
    """Outbound DTO – shape of a product returned by the API."""

    id: int
    name: str
    sku: str
    price: float
    quantity: int
    category: ProductCategory
    description: Optional[str] = None
    releaseDate: Optional[date] = None
    inStock: bool

    @classmethod
    def from_entity(cls, product: Product) -> "ProductResponseDTO":
        return cls(
            id=product.id,
            name=product.name,
            sku=product.sku,
            price=product.price,
            quantity=product.quantity,
            category=product.category,
            description=product.description,
            releaseDate=product.release_date,
            inStock=product.in_stock,
        )
