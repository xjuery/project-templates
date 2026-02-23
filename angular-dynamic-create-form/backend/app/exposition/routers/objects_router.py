"""
Dynamic exposition router.

A single router handles all object types.  The URL path segment
``{resource}`` (e.g. "persons", "products") is matched at runtime against
the ObjectTypeConfig registry loaded from the domain JSON files.

Endpoints:
    GET    /{resource}        – list all records
    POST   /{resource}        – create a new record
    DELETE /{resource}/{id}   – delete a record
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.application.dtos.dynamic_dto import build_create_model, build_response_model
from app.application.use_cases.create_object import CreateObject
from app.application.use_cases.delete_object import DeleteObject
from app.application.use_cases.get_all_objects import GetAllObjects
from app.domain.entities.field_config import ObjectTypeConfig
from app.domain.repositories.object_config_repository import ObjectConfigRepository
from app.domain.repositories.object_repository import ObjectRepository
from app.exposition.dependencies import get_config_repository, get_object_repository

router = APIRouter(tags=["objects"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_config(
    resource: str,
    config_repo: ObjectConfigRepository,
) -> ObjectTypeConfig:
    """Look up the ObjectTypeConfig for *resource*, or raise 404."""
    config = config_repo.find_by_resource(resource)
    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown resource '{resource}'. "
                   f"Available: {[c.resource for c in config_repo.find_all()]}",
        )
    return config


def _resolve_repo(
    config: ObjectTypeConfig,
) -> ObjectRepository:
    try:
        return get_object_repository(config.object_type)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/{resource}", status_code=status.HTTP_200_OK)
def list_objects(
    resource: str,
    config_repo: ObjectConfigRepository = Depends(get_config_repository),
) -> List[Dict[str, Any]]:
    """Return all records for the given resource."""
    config = _resolve_config(resource, config_repo)
    repo = _resolve_repo(config)
    return GetAllObjects(repo).execute()


@router.post("/{resource}", status_code=status.HTTP_201_CREATED)
async def create_object(
    resource: str,
    request: Request,
    config_repo: ObjectConfigRepository = Depends(get_config_repository),
) -> Dict[str, Any]:
    """Create a new record for the given resource.

    The request body is validated at runtime against the Pydantic model
    generated from the ObjectTypeConfig, mirroring the Angular form validation.
    """
    config = _resolve_config(resource, config_repo)
    repo = _resolve_repo(config)

    body: Dict[str, Any] = await request.json()
    CreateModel = build_create_model(config)

    try:
        validated = CreateModel.model_validate(body)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors(),
        ) from exc

    data = validated.model_dump()
    return CreateObject(repo).execute(data)


@router.delete("/{resource}/{obj_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_object(
    resource: str,
    obj_id: int,
    config_repo: ObjectConfigRepository = Depends(get_config_repository),
) -> None:
    """Delete a record by id."""
    config = _resolve_config(resource, config_repo)
    repo = _resolve_repo(config)

    deleted = DeleteObject(repo).execute(obj_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {config.display_name} with id {obj_id}.",
        )
