from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class PersonRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    GUEST = "guest"


@dataclass
class Person:
    first_name: str
    last_name: str
    nickname: str
    email: str
    role: PersonRole
    id: Optional[int] = field(default=None)
    birth_date: Optional[date] = field(default=None)
    age: Optional[int] = field(default=None)
    bio: Optional[str] = field(default=None)
    is_active: bool = field(default=True)
