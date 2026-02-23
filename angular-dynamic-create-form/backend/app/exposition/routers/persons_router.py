from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.person_dto import CreatePersonDTO, PersonResponseDTO
from app.application.use_cases.person.create_person import CreatePerson
from app.application.use_cases.person.delete_person import DeletePerson
from app.application.use_cases.person.get_all_persons import GetAllPersons
from app.exposition.dependencies import get_person_repository
from app.domain.repositories.person_repository import PersonRepository

router = APIRouter(prefix="/persons", tags=["persons"])


def _get_all_persons_uc(repo: PersonRepository = Depends(get_person_repository)) -> GetAllPersons:
    return GetAllPersons(repo)


def _create_person_uc(repo: PersonRepository = Depends(get_person_repository)) -> CreatePerson:
    return CreatePerson(repo)


def _delete_person_uc(repo: PersonRepository = Depends(get_person_repository)) -> DeletePerson:
    return DeletePerson(repo)


@router.get("", response_model=List[PersonResponseDTO], status_code=status.HTTP_200_OK)
def list_persons(use_case: GetAllPersons = Depends(_get_all_persons_uc)) -> List[PersonResponseDTO]:
    """Return all persons."""
    persons = use_case.execute()
    return [PersonResponseDTO.from_entity(p) for p in persons]


@router.post("", response_model=PersonResponseDTO, status_code=status.HTTP_201_CREATED)
def create_person(
    payload: CreatePersonDTO,
    use_case: CreatePerson = Depends(_create_person_uc),
) -> PersonResponseDTO:
    """Create a new person."""
    person = use_case.execute(payload.to_entity())
    return PersonResponseDTO.from_entity(person)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: int,
    use_case: DeletePerson = Depends(_delete_person_uc),
) -> None:
    """Delete a person by id."""
    deleted = use_case.execute(person_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {person_id} not found.",
        )
