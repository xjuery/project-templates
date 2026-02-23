# Angular Dynamic Create Form

A full-stack **schema-driven object manager**: create forms, list views, REST endpoints, and database tables are all generated at runtime from a single JSON configuration file per entity type. Adding a new object type requires no code changes in either the frontend or the backend — only a JSON file.

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Angular 21 SPA           FastAPI backend          │
│   port 4200          ←→    port 8000                │
│                                                     │
│   • Dynamic forms          • Dynamic endpoints      │
│   • Dynamic tables         • Dynamic validation     │
│   • PrimeNG UI             • SQLite (SQLAlchemy)    │
│                                                     │
│   Both driven by the same  *.json  config files     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Table of contents

1. [Repository layout](#repository-layout)
2. [Quick start](#quick-start)
3. [How the two apps connect](#how-the-two-apps-connect)
4. [Available URLs](#available-urls)
5. [Makefile reference](#makefile-reference)
6. [The JSON config files — single source of truth](#the-json-config-files--single-source-of-truth)
7. [Further reading](#further-reading)

---

## Repository layout

```
angular-dynamic-create-form/
│
├── frontend/                  Angular 21 SPA
│   └── README.md              → frontend architecture & config file reference
│
├── backend/                   FastAPI + SQLite API
│   └── README.md              → backend architecture & API reference
│
├── mockserver/                Legacy json-server (kept for reference / offline use)
│
└── Makefile                   All developer commands (see below)
```

---

## Quick start

### Prerequisites

| Tool | Minimum version | Used by |
|---|---|---|
| Node.js | 18 LTS | frontend, mockserver |
| npm | 9 | frontend, mockserver |
| Python | 3.11 | backend |
| GNU make | 3.81 | Makefile targets |

### First-time setup

```bash
# Clone the repository and install all dependencies in one command
make install
```

This runs `npm install` in `frontend/` and `mockserver/`, and creates a Python virtual environment in `backend/.venv` with all Python packages installed.

### Start the development environment

```bash
make dev
```

This launches the Angular dev server and the FastAPI backend in parallel. Both use auto-reload — any file change restarts the relevant process automatically.

---

## How the two apps connect

The Angular dev server proxies every request whose path starts with `/api` to the FastAPI backend, stripping the prefix before forwarding:

```
Browser
  └─ Angular dev server (port 4200)
        └─ /api/* requests → proxy (proxy.conf.backend.json)
                └─ http://localhost:8000/*  (FastAPI)
                        └─ SQLite (dynamic_form.db)
```

For example, when the user saves a new person the following chain is triggered:

```
Angular POST /api/persons
  → proxy strips /api → FastAPI POST /persons
      → validated against rules from person.json
          → written to the `person` table in dynamic_form.db
              → response id returned to Angular
```

The Angular proxy configuration lives in [`frontend/proxy.conf.backend.json`](frontend/proxy.conf.backend.json).
No changes to that file are needed when adding a new object type.

### Legacy mock server

A [json-server](https://github.com/typicode/json-server) mock is kept in `mockserver/` for offline development or quick prototyping.
To use it instead of the FastAPI backend:

```bash
make dev-mock   # starts Angular (proxied to json-server) + json-server
```

---

## Available URLs

| URL | Description |
|---|---|
| `http://localhost:4200` | Angular SPA |
| `http://localhost:4200/objects/person/create` | Create a new person |
| `http://localhost:4200/objects/person/list` | List all persons |
| `http://localhost:4200/objects/product/create` | Create a new product |
| `http://localhost:4200/objects/product/list` | List all products |
| `http://localhost:8000` | FastAPI root |
| `http://localhost:8000/docs` | Swagger UI (interactive API docs) |
| `http://localhost:8000/health` | Health check endpoint |
| `http://localhost:3001` | json-server mock (when using `make dev-mock`) |

---

## Makefile reference

Run `make help` for a formatted summary. The most frequently used targets:

### Installation

| Target | Description |
|---|---|
| `make install` | Install all dependencies (frontend, backend, mockserver) |
| `make install-frontend` | Install Angular dependencies only |
| `make install-backend` | Create Python venv and install FastAPI dependencies |
| `make install-mock` | Install json-server dependencies only |

### Development

| Target | Description |
|---|---|
| `make dev` | Start Angular (proxied to FastAPI) **+** FastAPI in parallel |
| `make dev-mock` | Start Angular (proxied to json-server) **+** json-server in parallel |
| `make start-frontend` | Start Angular dev server only (proxied to FastAPI) |
| `make start-backend` | Start FastAPI backend only |
| `make start-mock` | Start json-server mock only |

### Build & quality

| Target | Description |
|---|---|
| `make build` | Production build of the Angular app (`frontend/dist/`) |
| `make lint` | Run the Angular ESLint linter |
| `make format` | Format frontend source with Prettier |

### Maintenance

| Target | Description |
|---|---|
| `make reset-data` | Wipe `mockserver/db.json` back to empty arrays |
| `make clean` | Remove `frontend/dist/` |
| `make clean-all` | Remove `dist/`, `node_modules/` everywhere, and `backend/.venv` |

---

## The JSON config files — single source of truth

Every entity type is described by a single JSON file. The **same file** is read by both applications:

| Application | Location |
|---|---|
| Angular frontend | `frontend/public/assets/object-types/<type>.json` |
| FastAPI backend | `backend/app/domain/object_types/<type>.json` |

Both files must be kept in sync (or symlinked). The schema is documented in full in the frontend README — see [Object-type configuration files](frontend/README.md#object-type-configuration-files).

A minimal example:

```json
{
  "objectType": "invoice",
  "displayName": "Invoice",
  "apiEndpoint": "/api/invoices",
  "fields": [
    { "name": "number",  "label": "Invoice #", "type": "text",    "required": true },
    { "name": "amount",  "label": "Amount",    "type": "number",  "required": true, "min": 0 },
    { "name": "dueDate", "label": "Due Date",  "type": "date",    "required": true },
    { "name": "paid",    "label": "Paid",      "type": "boolean", "default": false  }
  ]
}
```

What happens automatically after adding this file and restarting both servers:

| Layer | What is generated |
|---|---|
| Angular | Create form and list view for `invoice` (after adding it to the sidebar nav) |
| FastAPI | `GET /invoices`, `POST /invoices`, `DELETE /invoices/{id}` endpoints |
| SQLite | `invoice` table with the matching columns and constraints |

For the step-by-step procedure see:
- Frontend: [Adding a new object type](frontend/README.md#adding-a-new-object-type)
- Backend: [Adding a new object type](backend/README.md#adding-a-new-object-type)

---

## Further reading

| Document | Contents |
|---|---|
| [`frontend/README.md`](frontend/README.md) | Angular architecture, component breakdown, dynamic form internals, config file schema, adding new types on the frontend |
| [`backend/README.md`](backend/README.md) | Hexagonal architecture layers, Python project structure, dynamic table generation, API reference, adding new types on the backend |
