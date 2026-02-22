# CLAUDE.md — Angular Advanced Search App

## Development Commands

```bash
# ── Frontend (Angular) — run from frontend/ ─────────────────────────
cd frontend
npm install          # first-time setup
npm start            # Angular dev server → http://localhost:4200
npm run build        # production build → frontend/dist/angular-search-app/
npm test             # Karma/Jasmine unit tests

# ── Backend (FastAPI) — run from backend/ ───────────────────────────
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# API available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

Both processes must run simultaneously in development.
Always run `npm run build` from `frontend/` after significant changes to catch TypeScript errors.

## Repository Structure

```
angular-advanced-search/
├── frontend/                       # Angular 20 application
│   ├── src/app/
│   │   ├── models/
│   │   │   └── search.models.ts    # All shared TS types and operator definitions
│   │   ├── services/
│   │   │   └── search.service.ts   # HttpClient wrapper; calls http://localhost:8000/api
│   │   ├── components/
│   │   │   └── filter-builder/     # Standalone reusable filter-row component
│   │   └── pages/
│   │       └── search/             # Single page: filter builder + results table
│   ├── angular.json
│   └── package.json
│
└── backend/                        # FastAPI application (Hexagonal Architecture)
    ├── app/
    │   ├── main.py                 # FastAPI app, CORS, router mounting
    │   ├── domain/                 # ── Domain Layer ──────────────────────────
    │   │   ├── entities.py         # Employee, FieldDefinition
    │   │   ├── value_objects.py    # SearchFilter, SearchQuery, SearchResult
    │   │   └── ports/
    │   │       └── employee_repository.py  # Abstract port (interface)
    │   ├── application/            # ── Application Layer ─────────────────────
    │   │   └── use_cases/
    │   │       ├── get_fields.py           # GetFieldsUseCase
    │   │       ├── search_employees.py     # SearchEmployeesUseCase
    │   │       └── export_csv.py           # ExportCsvUseCase
    │   ├── exposition/             # ── Exposition Layer (primary adapter) ────
    │   │   ├── schemas.py          # Pydantic request/response models
    │   │   ├── dependencies.py     # FastAPI DI wiring
    │   │   └── routers/
    │   │       ├── fields_router.py    # GET /api/fields
    │   │       └── search_router.py    # POST /api/search, POST /api/search/export
    │   └── infrastructure/         # ── Infrastructure Layer (secondary adapter)
    │       ├── sample_data.py      # 30 employee records + field definitions
    │       └── repositories/
    │           └── in_memory_employee_repository.py  # Implements the port
    └── requirements.txt
```

## Hexagonal Architecture (Backend)

The backend follows the Ports & Adapters pattern described by Alistair Cockburn:

| Layer | Role | Dependencies |
|-------|------|--------------|
| **Domain** | Core entities and value objects. Pure Python, zero framework imports. | None |
| **Application** | Use cases / business logic. Orchestrates domain objects via ports. | Domain only |
| **Exposition** | Driving adapter. FastAPI routes, Pydantic schemas, HTTP translation. | Application |
| **Infrastructure** | Driven adapter. In-memory repository, sample data. Implements ports. | Domain |

**The golden rule:** inner layers never import from outer ones.
`domain → application → exposition` and `infrastructure` implements the domain port.

## API Contract

### `GET /api/fields`
Returns `FieldDefinition[]`:
```json
[{ "field": "name", "label": "Name", "type": "string" }]
```

### `POST /api/search`
Request body — `SearchQuerySchema`:
```json
{
  "text": "alice",
  "filters": [{ "id": "uuid", "field": "age", "operator": "greater_than", "value": 30 }],
  "combinator": "and",
  "page": 1,
  "pageSize": 10,
  "sortField": "name",
  "sortOrder": "asc"
}
```
Response — `SearchResponseSchema`:
```json
{ "data": [...], "total": 15, "page": 1, "pageSize": 10, "totalPages": 2 }
```

### `POST /api/search/export`
Same body as `/api/search`. Returns `text/csv` as a file download (no pagination).

Interactive docs: `http://localhost:8000/docs`

## Key Angular Architectural Decisions

### Standalone Components Only
All components use `standalone: true`. No NgModules. Imports are declared per-component.

### Lazy-loaded Routes
Pages are lazy-loaded via `loadComponent` in `app.routes.ts`. Do not eagerly import page components.

### State in SearchService
`SearchService` stores the current `SearchQuery` in a `BehaviorSubject`. Do not use query params or router state for this.

### Server-side Everything
Filtering, sorting, and pagination are all handled by the FastAPI backend. The Angular table uses `[lazy]="true"` and fires `(onLazyLoad)` events. Do not implement client-side filtering.

### PrimeNG Theme
Using the **Aura** preset from `@primeng/themes`. Theme is configured once in `app.config.ts` via `providePrimeNG()`. Dark mode is toggled by `ThemeService` which:
- Adds/removes `.dark-mode` on `<html>` (PrimeNG's `darkModeSelector`)
- Sets `html.style.colorScheme` to `'dark'/'light'` for native browser elements
- Persists the preference in `localStorage`; falls back to `prefers-color-scheme`

**Do NOT add `cssLayer` to the `providePrimeNG` options** — that configuration is only for Tailwind CSS integration. Without Tailwind, it wraps PrimeNG component styles in `@layer primeng`, which loses to unlayered browser-default styles (white input backgrounds, etc.), breaking dark mode for native elements.

## Adding New Fields to the Dataset

1. Add the attribute to `Employee` in `backend/app/domain/entities.py` and update `to_dict()`
2. Add the field data to `EMPLOYEES` and a `FieldDefinition` to `FIELD_DEFINITIONS` in `backend/app/infrastructure/sample_data.py`
3. Update filter logic in `InMemoryEmployeeRepository._apply_filter()` if the type is new

No frontend changes needed — field definitions are fetched dynamically from `/api/fields`.

## Adding a New Filter Operator

1. Add the operator object to the relevant `*_OPERATORS` array in `frontend/src/app/models/search.models.ts`
2. Add the corresponding `case` in the appropriate `_filter_*` method in `InMemoryEmployeeRepository`
3. If the operator needs no value input (like `is_empty`), add it to `needsValueInput()` in `search.models.ts`

## Frontend Conventions (Angular / PrimeNG)

- Use `inject()` over constructor injection for all services
- Use Angular 17+ control flow (`@if`, `@for`, `@switch`) — avoid `*ngIf` / `*ngFor` directives
- Use `crypto.randomUUID()` for filter IDs (no external UUID library needed)
- SCSS follows BEM naming: `.block__element--modifier`
- Use PrimeNG CSS custom properties (`var(--p-surface-0)`, `var(--p-primary-color)`, etc.) for theming — do not hardcode colors
- Use `styleClass` prop (not `class`) to add CSS classes to PrimeNG components
- Use `::ng-deep` inside the component's SCSS to target PrimeNG internal elements — scope it under `:host`
- Import PrimeNG modules individually per component (e.g., `ButtonModule`, `SelectModule`)
- `MessageService` must be provided at the component level (`providers: [MessageService]`) alongside `ToastModule`
- Prettier is configured: `printWidth: 100`, `singleQuote: true`

## Version Pinning Notes

PrimeNG and Angular versions must stay in sync:

| Angular | PrimeNG | @primeng/themes |
|---------|---------|-----------------|
| ^20.x   | ^20.x   | ^20.x           |
| ^21.x   | ^21.x   | ^21.x           |

Installing mismatched majors causes peer dependency errors. Use `npm install primeng@20 @primeng/themes@20` explicitly.
