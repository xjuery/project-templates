"""
Exposition Layer — Fields Router

Exposes GET /api/fields, which returns the list of field definitions so the
Angular filter builder can dynamically render type-aware filter rows.
"""

from fastapi import APIRouter, Depends

from app.application.use_cases.get_fields import GetFieldsUseCase
from app.exposition.dependencies import get_fields_use_case
from app.exposition.schemas import FieldDefinitionSchema

router = APIRouter()


@router.get("/fields", response_model=list[FieldDefinitionSchema])
def get_fields(use_case: GetFieldsUseCase = Depends(get_fields_use_case)):
    fields = use_case.execute()
    return [{"field": f.field, "label": f.label, "type": f.type} for f in fields]
