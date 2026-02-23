from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.domain.entities.person import Person, PersonRole


class CreatePersonDTO(BaseModel):
    """Inbound DTO – validated data coming from the API request."""

    firstName: str = Field(..., min_length=2, max_length=50)
    lastName: str = Field(..., min_length=2, max_length=50)
    nickname: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    role: PersonRole
    birthDate: Optional[date] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)
    bio: Optional[str] = Field(default=None, max_length=500)
    isActive: bool = True

    def to_entity(self) -> Person:
        return Person(
            first_name=self.firstName,
            last_name=self.lastName,
            nickname=self.nickname,
            email=self.email,
            role=self.role,
            birth_date=self.birthDate,
            age=self.age,
            bio=self.bio,
            is_active=self.isActive,
        )


class PersonResponseDTO(BaseModel):
    """Outbound DTO – shape of a person returned by the API."""

    id: int
    firstName: str
    lastName: str
    nickname: str
    email: str
    role: PersonRole
    birthDate: Optional[date] = None
    age: Optional[int] = None
    bio: Optional[str] = None
    isActive: bool

    @classmethod
    def from_entity(cls, person: Person) -> "PersonResponseDTO":
        return cls(
            id=person.id,
            firstName=person.first_name,
            lastName=person.last_name,
            nickname=person.nickname,
            email=person.email,
            role=person.role,
            birthDate=person.birth_date,
            age=person.age,
            bio=person.bio,
            isActive=person.is_active,
        )
