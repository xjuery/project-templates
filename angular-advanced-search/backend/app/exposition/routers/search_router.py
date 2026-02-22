"""
Exposition Layer — Search Router

Exposes two endpoints:
  POST /api/search         — paginated search, returns JSON
  POST /api/search/export  — same query but returns a CSV file download
"""

import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.application.use_cases.export_csv import ExportCsvUseCase
from app.application.use_cases.search_employees import SearchEmployeesUseCase
from app.domain.value_objects import SearchFilter, SearchQuery
from app.exposition.dependencies import get_export_use_case, get_search_use_case
from app.exposition.schemas import SearchQuerySchema, SearchResponseSchema

router = APIRouter()


def _to_domain_query(schema: SearchQuerySchema) -> SearchQuery:
    """Translate the HTTP schema (camelCase) into the domain value object (snake_case)."""
    filters = tuple(
        SearchFilter(id=f.id, field=f.field, operator=f.operator, value=f.value)
        for f in schema.filters
    )
    return SearchQuery(
        text=schema.text,
        filters=filters,
        combinator=schema.combinator,
        page=schema.page,
        page_size=schema.pageSize,
        sort_field=schema.sortField,
        sort_order=schema.sortOrder,
    )


@router.post("/search", response_model=SearchResponseSchema)
def search(
    body: SearchQuerySchema,
    use_case: SearchEmployeesUseCase = Depends(get_search_use_case),
):
    query = _to_domain_query(body)
    result = use_case.execute(query)
    return {
        "data": list(result.data),
        "total": result.total,
        "page": result.page,
        "pageSize": result.page_size,
        "totalPages": result.total_pages,
    }


@router.post("/search/export")
def export_csv(
    body: SearchQuerySchema,
    use_case: ExportCsvUseCase = Depends(get_export_use_case),
):
    """Return a CSV file containing all records matching the query (no pagination)."""
    query = _to_domain_query(body)
    csv_content = use_case.execute(query)
    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=search-results.csv"},
    )
