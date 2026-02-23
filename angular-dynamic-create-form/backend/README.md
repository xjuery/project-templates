# Object Manager — FastAPI Backend

A **schema-driven REST API** built with FastAPI and Python 3.11.
Every object type (its fields, validation rules, and database table) is generated at startup from the same JSON configuration files that drive the Angular frontend — **no Python code changes are needed to support a new entity**.

Built with **FastAPI**, **Pydantic v2**, **SQLModel** and **SQLAlchemy Core**, persisting data in a **SQLite** database.

---

## Table of contents

1. [Requirements](#requirements)
2. [Getting started](#getting-started)
3. [Architecture — Hexagonal (Ports & Adapters)](#architecture--hexagonal-ports--adapters)
4. [Project structure](#project-structure)
5. [How the dynamic system works](#how-the-dynamic-system-works)
6. [API reference](#api-reference)
7. [Adding a new object type](#adding-a-new-object-type)
8. [Database](#database)
9. [Development commands](#development-commands)

---

## Requirements

| Tool | Minimum version |
|---|---|
| Python | 3.11 |
| pip | 23+ |

All Python dependencies are declared in [`requirements.txt`](requirements.txt) and [`pyproject.toml`](pyproject.toml).

---

## Getting started

> The Makefile at the repository root is the recommended way to run the project.
> See the [root README](../README.md) or run `make help` from there.

To run the backend on its own:

```bash
# Create the virtual environment and install dependencies
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Start the development server (auto-reload enabled)
.venv/bin/uvicorn main:app --reload --port 8000
```

Or, using the Makefile from the repository root:

```bash
make install-backend   # first-time setup
make start-backend     # start the server
```

The API will be available at `http://localhost:8000`.
Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

---

## Architecture — Hexagonal (Ports & Adapters)

The application follows the **Hexagonal Architecture** pattern described by Alistair Cockburn (also known as *Ports & Adapters*). The goal is a strict separation of concerns: the business core is isolated from all infrastructure details (database, file system, HTTP framework).

```
┌──────────────────────────────────────────────────────────────┐
│                        Application core                       │
│                                                              │
│   ┌──────────────────────────────────────────────────────┐  │
│   │                   Domain Layer                        │  │
│   │  Entities (FieldConfig, ObjectTypeConfig)             │  │
│   │  Repository ports (abstract interfaces)               │  │
│   │  JSON config files (object_types/*.json)              │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                              │
│   ┌──────────────────────────────────────────────────────┐  │
│   │                 Application Layer                     │  │
│   │  Use cases: GetAllObjects, CreateObject, DeleteObject │  │
│   │  Dynamic DTO builder (Pydantic model factory)         │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                              │
└───────────────────────────┬──────────────────────────────────┘
                            │
          ┌─────────────────┴────────────────────┐
          │                                       │
┌─────────▼──────────┐              ┌─────────────▼──────────┐
│  Exposition Layer  │              │  Infrastructure Layer  │
│  (primary adapter) │              │  (secondary adapter)   │
│                    │              │                        │
│  FastAPI router    │              │  FileObjectConfig-     │
│  (dynamic          │              │  Repository            │
│   /{resource}      │              │  (reads JSON files)    │
│   endpoints)       │              │                        │
│                    │              │  SQLiteObjectRepository│
│  Pydantic          │              │  (SQLAlchemy Core)     │
│  validation        │              │                        │
│  at request time   │              │  TableRegistry         │
│                    │              │  (builds schema from   │
└────────────────────┘              │   FieldConfig)         │
                                    └────────────────────────┘
```

### Domain Layer

Contains the **core concepts** of the application. Nothing here depends on FastAPI, SQLAlchemy, or any other framework.

| File | Role |
|---|---|
| [`entities/field_config.py`](app/domain/entities/field_config.py) | `FieldConfig` and `ObjectTypeConfig` dataclasses — the Python mirror of the TypeScript interfaces in the frontend |
| [`repositories/object_config_repository.py`](app/domain/repositories/object_config_repository.py) | Abstract port for loading object-type configurations |
| [`repositories/object_repository.py`](app/domain/repositories/object_repository.py) | Abstract port for generic CRUD operations (records as plain `dict`) |
| [`object_types/person.json`](app/domain/object_types/person.json) | Configuration for the Person entity (shared with the frontend) |
| [`object_types/product.json`](app/domain/object_types/product.json) | Configuration for the Product entity (shared with the frontend) |

The JSON files are the **single source of truth** for both the frontend form generation and the backend table schema and validation.

### Application Layer

Contains the **use cases** (business logic). Each use case receives a repository port via constructor injection and operates on plain `dict` objects — it knows nothing about HTTP or SQL.

| File | Role |
|---|---|
| [`use_cases/get_all_objects.py`](app/application/use_cases/get_all_objects.py) | Retrieve all records for an object type |
| [`use_cases/create_object.py`](app/application/use_cases/create_object.py) | Persist a validated new record |
| [`use_cases/delete_object.py`](app/application/use_cases/delete_object.py) | Delete a record by id |
| [`dtos/dynamic_dto.py`](app/application/dtos/dynamic_dto.py) | Builds typed Pydantic `BaseModel` subclasses at runtime from an `ObjectTypeConfig` |

### Infrastructure Layer

Contains the **adapters** that satisfy the domain ports using concrete technologies.

| File | Role |
|---|---|
| [`config/file_object_config_repository.py`](app/infrastructure/config/file_object_config_repository.py) | Reads `*.json` files from `domain/object_types/` and parses them into `ObjectTypeConfig` instances |
| [`database/engine.py`](app/infrastructure/database/engine.py) | Creates the SQLite engine via `sqlmodel.create_engine` |
| [`database/table_registry.py`](app/infrastructure/database/table_registry.py) | Converts each `FieldConfig` into a SQLAlchemy `Column` and registers a `Table` in the shared `MetaData` |
| [`repositories/sqlite_object_repository.py`](app/infrastructure/repositories/sqlite_object_repository.py) | Implements the `ObjectRepository` port using SQLAlchemy Core (no ORM classes) |

### Exposition Layer

Contains the **primary adapter** — the FastAPI HTTP interface.

| File | Role |
|---|---|
| [`routers/objects_router.py`](app/exposition/routers/objects_router.py) | Single dynamic `APIRouter` with three endpoints: `GET /{resource}`, `POST /{resource}`, `DELETE /{resource}/{id}` |
| [`dependencies.py`](app/exposition/dependencies.py) | Bootstrap module: loads configs, registers tables, creates the SQLite schema, instantiates one repository per object type |

---

## Project structure

```
backend/
├── main.py                          FastAPI application factory
├── requirements.txt                 Runtime dependencies
├── pyproject.toml                   Project metadata + optional dev deps
├── dynamic_form.db                  SQLite database (created on first run)
│
└── app/
    │
    ├── domain/                      ── Core (no external dependencies) ──
    │   ├── object_types/
    │   │   ├── person.json          Object-type configs (shared with frontend)
    │   │   └── product.json
    │   ├── entities/
    │   │   └── field_config.py      FieldConfig, ObjectTypeConfig, SelectOption
    │   └── repositories/
    │       ├── object_config_repository.py   Abstract port: load configs
    │       └── object_repository.py          Abstract port: CRUD on dicts
    │
    ├── application/                 ── Business logic ──
    │   ├── dtos/
    │   │   └── dynamic_dto.py       Pydantic model builder (create + response)
    │   └── use_cases/
    │       ├── get_all_objects.py
    │       ├── create_object.py
    │       └── delete_object.py
    │
    ├── infrastructure/              ── Adapters (secondary / driven) ──
    │   ├── config/
    │   │   └── file_object_config_repository.py   Reads JSON files from disk
    │   ├── database/
    │   │   ├── engine.py            SQLite engine (SQLModel)
    │   │   └── table_registry.py    FieldConfig → Column, Table, MetaData
    │   └── repositories/
    │       └── sqlite_object_repository.py        SQLAlchemy Core CRUD
    │
    └── exposition/                  ── Adapter (primary / driving) ──
        ├── dependencies.py          DI wiring + startup bootstrap
        └── routers/
            └── objects_router.py    Dynamic /{resource} endpoints
```

---

## How the dynamic system works

### 1. Startup bootstrap (`dependencies.py`)

When the server starts, `app/exposition/dependencies.py` is imported, triggering the following sequence:

```
Load *.json files from domain/object_types/
        │
        ▼
Parse each file → ObjectTypeConfig (with a list of FieldConfig)
        │
        ▼
For each config, build a SQLAlchemy Table:
  id      INTEGER PRIMARY KEY AUTOINCREMENT
  <field> <SQLAlchemy type>  NULL|NOT NULL   ← derived from FieldConfig
        │
        ▼
metadata.create_all(engine)  →  CREATE TABLE IF NOT EXISTS …
        │
        ▼
Instantiate one SQLiteObjectRepository per table
```

### 2. Field type mapping

| JSON `type` | SQLAlchemy column | Python / Pydantic type |
|---|---|---|
| `text` | `String(maxLength \| 255)` | `str` |
| `email` | `String(254)` | `EmailStr` |
| `number` | `Float` | `float` |
| `date` | `Date` | `datetime.date` |
| `boolean` | `Boolean` | `bool` |
| `select` | `String(100)` | `Literal['opt1', 'opt2', …]` |
| `textarea` | `Text` | `str` |

### 3. Request validation (`dynamic_dto.py`)

For every `POST /{resource}` request the router:

1. Looks up the `ObjectTypeConfig` for the resource.
2. Calls `build_create_model(config)` which uses `pydantic.create_model()` to produce a typed `BaseModel` class — including `min_length`, `max_length`, `ge`, `le`, `pattern`, and enum `Literal` constraints from the JSON config.
3. Calls `Model.model_validate(body)` on the raw JSON body.
4. On failure a `422 Unprocessable Entity` response is returned with Pydantic's structured error list.
5. On success the validated data is passed to the `CreateObject` use case.

### 4. Dynamic routing (`objects_router.py`)

A single `/{resource}` path parameter is matched at runtime:

```python
@router.get("/{resource}")
def list_objects(resource: str, ...):
    config = config_repo.find_by_resource(resource)  # e.g. "persons" → person config
    repo   = get_object_repository(config.object_type)
    return GetAllObjects(repo).execute()
```

The mapping from `resource` (URL segment like `"persons"`) to `object_type` (like `"person"`) is driven by the `apiEndpoint` field in the JSON config file.

---

## API reference

All endpoints are documented interactively at `http://localhost:8000/docs` (Swagger UI).

### List all records

```
GET /{resource}
```

Returns a JSON array of all records for the resource. Returns `[]` when empty.

**Example**

```bash
curl http://localhost:8000/persons
```

### Create a record

```
POST /{resource}
Content-Type: application/json
```

Validates the body against the rules defined in the JSON config and persists the record. Returns the created object with its assigned `id`.

**Response codes**

| Code | Meaning |
|---|---|
| `201 Created` | Record created successfully |
| `404 Not Found` | Unknown resource |
| `422 Unprocessable Entity` | Validation error (body contains detailed error list) |

**Example**

```bash
curl -X POST http://localhost:8000/persons \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Alice",
    "lastName":  "Smith",
    "nickname":  "ali",
    "email":     "alice@example.com",
    "role":      "admin",
    "isActive":  true
  }'
```

### Delete a record

```
DELETE /{resource}/{id}
```

| Code | Meaning |
|---|---|
| `204 No Content` | Record deleted |
| `404 Not Found` | Unknown resource or id not found |

**Example**

```bash
curl -X DELETE http://localhost:8000/persons/1
```

### Health check

```
GET /health
```

Returns `{"status": "ok"}`. Useful for readiness probes.

---

## Adding a new object type

Adding a new entity requires **no Python changes** — only a JSON file and a restart.

### Step 1 — Create the config file

Drop a new file in `app/domain/object_types/<yourtype>.json`.
The schema is identical to the frontend config (see the frontend [Object-type configuration files](../frontend/README.md#object-type-configuration-files) section for the full field reference):

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

### Step 2 — Restart the server

On next startup the bootstrap sequence will:

- Create an `invoice` table in SQLite with the matching columns.
- Register `GET /invoices`, `POST /invoices`, and `DELETE /invoices/{id}` endpoints automatically.
- Apply the validation rules defined in the JSON to all incoming `POST /invoices` requests.

### Step 3 — Add the config to the frontend too

Copy (or symlink) the same JSON file to
`../frontend/public/assets/object-types/invoice.json`
and follow the frontend's [Adding a new object type](../frontend/README.md#adding-a-new-object-type) steps.

---

## Database

The application uses **SQLite** stored in `backend/dynamic_form.db`.

- The file is created automatically on first startup.
- Tables are created with `CREATE TABLE IF NOT EXISTS` — restarting the server is safe even after the file already exists.
- Each JSON config file maps to **one table** whose name is the `objectType` value (e.g. `person`, `product`).
- Columns are named after the `name` field of each `FieldConfig` entry (camelCase, matching the JSON payload keys the frontend sends).

To **reset** the database, stop the server and delete the file:

```bash
rm backend/dynamic_form.db
```

The tables will be recreated (empty) on the next startup.

---

## Development commands

Run from the `backend/` directory (with the venv activated) or use the Makefile targets from the repository root.

| Command | Description |
|---|---|
| `make install-backend` | Create `.venv` and install all dependencies |
| `make start-backend` | Start uvicorn with `--reload` on port 8000 |
| `.venv/bin/uvicorn main:app --reload --port 8000` | Same, run directly |
| `make dev` | Start frontend **and** backend in parallel |
| `make clean-all` | Remove `.venv`, `node_modules`, and build artefacts everywhere |
