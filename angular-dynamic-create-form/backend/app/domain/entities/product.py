from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    OTHER = "other"


@dataclass
class Product:
    name: str
    sku: str
    price: float
    quantity: int
    category: ProductCategory
    id: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)
    release_date: Optional[date] = field(default=None)
    in_stock: bool = field(default=True)
