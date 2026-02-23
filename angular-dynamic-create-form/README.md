# Angular Dynamic Create Form

A full-stack object manager where **forms, list views, and REST endpoints are all generated at runtime from JSON configuration files**. Adding a new object type requires no code changes in either the frontend or the backend — only a JSON config file.

---

## Repository layout

```
angular-dynamic-create-form/
│
├── frontend/        Angular 21 SPA — dynamic forms and list views
│   └── README.md    → frontend architecture, component breakdown, config file schema
│
├── backend/         FastAPI REST API — hexagonal architecture, in-memory storage
│   └── README.md    → backend architecture, layer details, API reference
│
├── mockserver/      Legacy json-server (kept for offline / standalone use)
│
└── Makefile         All developer commands
```

---

## Quick start

### Prerequisites

| Tool | Minimum version | Used by |
|---|---|---|
| Node.js | 18 LTS | frontend, mockserver |
| npm | 9+ | frontend, mockserver |
| Python | 3.11+ | backend |
| GNU make | 3.81+ | Makefile targets |

### First-time setup

```bash
make install
```

This installs Angular and json-server dependencies (`npm install`) in `frontend/` and `mockserver/`, and creates a Python virtual environment in `backend/.venv` with all Python packages.

### Start the development environment

```bash
make dev
```

Launches the Angular dev server and the FastAPI backend in parallel. Both use hot-reload — file changes restart the relevant process automatically.

---

## How the two apps connect

The Angular dev server proxies every `/api/*` request to the FastAPI backend, stripping the prefix before forwarding:

```
Browser
  └─ Angular dev server  :4200
        └─ /api/* → proxy (proxy.conf.backend.json)
              └─ FastAPI  :8000  (path without /api prefix)
```

For example, saving a new person triggers:

```
Angular  POST /api/persons
  → proxy strips /api →  FastAPI  POST /persons
      → validated, stored in memory
          → 201 {"id": 1, "firstName": "Alice", ...}
```

The proxy configuration is in [`frontend/proxy.conf.backend.json`](frontend/proxy.conf.backend.json).

### Legacy mock server

`mockserver/` contains a [json-server](https://github.com/typicode/json-server) mock that was used before the FastAPI backend existed. To use it instead:

```bash
make dev-mock   # Angular (proxied to json-server) + json-server
```

---

## Available URLs

| URL | What it serves |
|---|---|
| `http://localhost:4200` | Angular SPA |
| `http://localhost:4200/objects/person/create` | Create person form |
| `http://localhost:4200/objects/person/list` | Person list |
| `http://localhost:4200/objects/product/create` | Create product form |
| `http://localhost:4200/objects/product/list` | Product list |
| `http://localhost:8000/docs` | Swagger UI — interactive API docs |
| `http://localhost:8000/health` | API health check |
| `http://localhost:3001` | json-server mock (only with `make dev-mock`) |

---

## Makefile reference

Run `make help` for a formatted, coloured summary in the terminal.

### Installation

| Target | Description |
|---|---|
| `make install` | Install all dependencies (frontend + backend + mockserver) |
| `make install-frontend` | `npm install` in `frontend/` |
| `make install-backend` | Create `backend/.venv` and install Python packages |
| `make install-mock` | `npm install` in `mockserver/` |

### Development

| Target | Description |
|---|---|
| `make dev` | Start Angular (→ FastAPI) **and** FastAPI in parallel |
| `make dev-mock` | Start Angular (→ json-server) **and** json-server in parallel |
| `make start-frontend` | Angular dev server only (proxied to FastAPI) |
| `make start-backend` | FastAPI backend only |
| `make start-frontend-mock` | Angular dev server only (proxied to json-server) |
| `make start-mock` | json-server only |

### Build & quality

| Target | Description |
|---|---|
| `make build` | Production build of the Angular app → `frontend/dist/` |
| `make lint` | Run the Angular ESLint linter |
| `make format` | Format Angular source files with Prettier |

### Maintenance

| Target | Description |
|---|---|
| `make reset-data` | Reset `mockserver/db.json` to empty collections |
| `make clean` | Delete `frontend/dist/` |
| `make clean-all` | Delete `dist/`, `node_modules/` everywhere, and `backend/.venv` |

---

## Further reading

| Document | What it covers |
|---|---|
| [`frontend/README.md`](frontend/README.md) | Angular architecture, how the dynamic form is built from config, the JSON config file schema and all supported field types, and the step-by-step guide to adding a new object type on the frontend side |
| [`backend/README.md`](backend/README.md) | Hexagonal architecture layers, project structure, request flow through the layers, the full API reference with field constraints, storage details, and the step-by-step guide to adding a new object type on the backend side |
