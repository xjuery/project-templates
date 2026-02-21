# CLAUDE.md — Angular Advanced Search App

## Development Commands

```bash
# Start everything (mock server + Angular dev server)
npm run dev

# Individual processes
npm run mock-server   # Express mock API on http://localhost:3000
npm start             # Angular dev server on http://localhost:4200

# Build & test
npm run build         # Production build → dist/angular-search-app/
npm test              # Karma/Jasmine unit tests
```

Always run `npm run build` after significant changes to catch TypeScript compilation errors before committing.

## Architecture Overview

Two processes must run simultaneously in development:

- **Mock server** (`mock-server/server.js`) — Node.js/Express on port 3000
- **Angular app** (`ng serve`) — on port 4200, calls the mock server via `HttpClient`

The mock server is the **sole data source**. It holds 30 sample employee records and handles all filtering, sorting, and pagination server-side.

## Project Structure

```
src/app/
├── models/
│   └── search.models.ts          # All shared types, interfaces, and operator definitions
├── services/
│   └── search.service.ts         # HttpClient wrapper; holds current query in BehaviorSubject
├── components/
│   └── filter-builder/           # Standalone reusable filter-row component
│       ├── filter-builder.component.ts
│       ├── filter-builder.component.html
│       └── filter-builder.component.scss
└── pages/
    ├── search/                   # /search route — text input + filter builder
    └── results/                  # /results route — sortable table + CSV export

mock-server/
└── server.js                     # Express API (GET /api/fields, POST /api/search)
```

## Key Architectural Decisions

### Standalone Components Only
All components use `standalone: true`. There are no NgModules. Imports are declared per-component.

### Lazy-loaded Routes
Both pages are lazy-loaded via `loadComponent` in `app.routes.ts`. Do not eagerly import page components.

### State Passing Between Pages
`SearchService` stores the current `SearchQuery` in a `BehaviorSubject`. The results page reads it on init and redirects to `/search` if no query is found. Do not use query params or router state for this.

### Server-side Everything
Filtering, sorting, and pagination are all handled by the mock server. The Angular table uses `[lazy]="true"` and fires `(onLazyLoad)` events. Do not implement client-side filtering.

### PrimeNG Theme
Using the **Aura** preset from `@primeng/themes`. Theme is configured once in `app.config.ts` via `providePrimeNG()`. Dark mode is toggled by adding `.dark-mode` to the `<html>` element.

## Adding New Fields to the Dataset

1. Add the field to each record object in `mock-server/server.js` (`SAMPLE_DATA` array)
2. Add its definition to `FIELD_DEFINITIONS` in the same file with the correct `type`
3. Add filter logic in the `applyFilter()` switch/case if the type is new

No Angular changes are needed — field definitions are fetched dynamically from `/api/fields`.

## Adding a New Filter Operator

1. Add the operator object to the relevant `*_OPERATORS` array in `src/app/models/search.models.ts`
2. Add the corresponding logic branch in `applyFilter()` in `mock-server/server.js`
3. If the operator needs no value input (like `is_empty`), add it to the `needsValueInput()` exclusion list in `search.models.ts`

## PrimeNG Component Conventions

- Use `styleClass` prop (not `class`) to add CSS classes to PrimeNG components
- Use `::ng-deep` inside the component's SCSS to target PrimeNG internal elements — scope it under `:host` to avoid leaking styles
- Import PrimeNG modules individually per component (e.g., `ButtonModule`, `SelectModule`), not a barrel import
- `MessageService` must be provided at the component level (`providers: [MessageService]`) alongside `ToastModule`

## API Contract

### `GET /api/fields`
Returns `FieldDefinition[]`:
```json
[{ "field": "name", "label": "Name", "type": "string" }]
```

### `POST /api/search`
Request body — `SearchQuery`:
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
Response — `SearchResponse`:
```json
{ "data": [...], "total": 15, "page": 1, "pageSize": 10, "totalPages": 2 }
```

## TypeScript & Style Conventions

- Use `inject()` over constructor injection for all services
- Use Angular 17+ control flow (`@if`, `@for`, `@switch`) — avoid `*ngIf` / `*ngFor` directives
- Use `crypto.randomUUID()` for filter IDs (no external UUID library needed)
- SCSS follows BEM naming: `.block__element--modifier`
- Use PrimeNG CSS custom properties (`var(--p-surface-0)`, `var(--p-primary-color)`, etc.) for theming — do not hardcode colors
- Prettier is configured: `printWidth: 100`, `singleQuote: true`

## Version Pinning Notes

PrimeNG and Angular versions must stay in sync:

| Angular | PrimeNG | @primeng/themes |
|---------|---------|-----------------|
| ^20.x   | ^20.x   | ^20.x           |
| ^21.x   | ^21.x   | ^21.x           |

Installing mismatched majors causes peer dependency errors. Use `npm install primeng@20 @primeng/themes@20` explicitly.
