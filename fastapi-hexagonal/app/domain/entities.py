from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    id: Optional[int]
    name: str
    description: Optional[str]


