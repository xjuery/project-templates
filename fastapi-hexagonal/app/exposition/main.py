from typing import List

from fastapi import Depends, FastAPI, HTTPException, status

from app.application.use_cases import ItemService
from app.domain.entities import Item
from .dependencies import get_item_service
from .schemas import ItemCreate, ItemRead


app = FastAPI(title="Hexagonal FastAPI Template", version="0.1.0")


@app.get("/health", tags=["health"])  # Simple health endpoint per FastAPI docs style
def health() -> dict:
    return {"status": "ok"}


@app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(payload: ItemCreate, service: ItemService = Depends(get_item_service)) -> Item:
    created = service.create_item(name=payload.name, description=payload.description)
    return created


@app.get("/items/{item_id}", response_model=ItemRead, tags=["items"])
def get_item(item_id: int, service: ItemService = Depends(get_item_service)) -> Item:
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.get("/items", response_model=List[ItemRead], tags=["items"])
def list_items(service: ItemService = Depends(get_item_service)) -> List[Item]:
    items = list(service.list_items())
    return items


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)) -> None:
    deleted = service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None


