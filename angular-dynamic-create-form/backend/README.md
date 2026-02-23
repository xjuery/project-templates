# Object Manager — FastAPI Backend

A REST API for the Angular Object Manager SPA, built with **FastAPI** and **Python 3.11**.

The internal architecture follows the **Hexagonal Architecture** pattern (Ports & Adapters) described by Alistair Cockburn, keeping the business core strictly isolated from the HTTP layer and the storage mechanism.

Data is stored **in memory** for the lifetime of the process — no database setup is required.

---

## Table of contents

1. [Requirements](#requirements)
2. [Getting started](#getting-started)
3. [Architecture — Hexagonal (Ports & Adapters)](#architecture--hexagonal-ports--adapters)
4. [Project structure](#project-structure)
5. [Request flow through the layers](#request-flow-through-the-layers)
6. [API reference](#api-reference)
7. [Storage](#storage)
8. [Development commands](#development-commands)

---

## Requirements

| Tool | Minimum version |
|---|---|
| Python | 3.11 |
| pip | 23+ |

All dependencies are declared in [`requirements.txt`](requirements.txt) and [`pyproject.toml`](pyproject.toml).

---

## Getting started

> The Makefile at the repository root is the recommended way to run the project.
> See the [root README](../README.md) or run `make help` from there.

To run the backend on its own:

```bash
# Create the virtual environment and install dependencies
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Start the development server (auto-reload on file changes)
.venv/bin/uvicorn main:app --reload --port 8000
```

Or via the Makefile from the repository root:

```bash
make install-backend   # one-time venv + dependency setup
make start-backend     # start the server
```

The API will be available at **`http://localhost:8000`**.
Interactive Swagger UI docs are available at **`http://localhost:8000/docs`**.

---

## Architecture — Hexagonal (Ports & Adapters)

The application is divided into four concentric layers. Dependencies only point **inward** — outer layers know about inner ones, never the reverse.

```
╔══════════════════════════════════════════════════════════════════╗
║                          Domain Layer                            ║
║   Pure Python dataclasses + abstract repository interfaces       ║
║   (no framework imports)                                         ║
╠══════════════════════════════════════════════════════════════════╣
║                        Application Layer                         ║
║   Use cases — one class per operation                            ║
║   Pydantic DTOs — inbound validation + outbound shaping          ║
╠═══════════════════════╦══════════════════════════════════════════╣
║   Exposition Layer    ║         Infrastructure Layer             ║
║   (primary adapter)   ║         (secondary adapter)              ║
║                       ║                                          ║
║   FastAPI routers     ║   In-memory repositories                 ║
║   HTTP endpoints      ║   (implement domain port ABCs)           ║
║   Pydantic request    ║   Thread-safe, auto-incrementing id       ║
║   / response models   ║                                          ║
╚═══════════════════════╩══════════════════════════════════════════╝
```

### Domain Layer — `app/domain/`

The innermost ring. Contains the business vocabulary and the abstract contracts (ports) for persistence. Nothing here imports FastAPI, Pydantic, or any other framework.

**Entities** (`app/domain/entities/`)

| File | Contents |
|---|---|
| [`person.py`](app/domain/entities/person.py) | `Person` dataclass + `PersonRole` enum (`admin`, `user`, `manager`, `guest`) |
| [`product.py`](app/domain/entities/product.py) | `Product` dataclass + `ProductCategory` enum (`electronics`, `clothing`, `food`, `books`, `other`) |

**Repository ports** (`app/domain/repositories/`)

Abstract base classes (ABC) that define the CRUD contract without any storage implementation. They are the *secondary ports* of the hexagon.

| File | Port interface |
|---|---|
| [`person_repository.py`](app/domain/repositories/person_repository.py) | `find_all()`, `find_by_id()`, `save()`, `delete()` |
| [`product_repository.py`](app/domain/repositories/product_repository.py) | same contract for `Product` |

### Application Layer — `app/application/`

Orchestrates the domain to fulfil use cases. Each use case class receives a repository port via its constructor (dependency injection) and calls only domain operations — it has no knowledge of HTTP or storage.

**Use cases** (`app/application/use_cases/`)

| Directory | Classes |
|---|---|
| `person/` | `GetAllPersons`, `CreatePerson`, `DeletePerson` |
| `product/` | `GetAllProducts`, `CreateProduct`, `DeleteProduct` |

**DTOs** (`app/application/dtos/`)

Pydantic v2 `BaseModel` classes that sit at the application boundary. They handle two responsibilities:

- *Inbound* (`Create*DTO`): validate the raw HTTP request body, enforce field constraints, and convert the validated data to a domain entity via `.to_entity()`.
- *Outbound* (`*ResponseDTO`): shape the domain entity into the JSON structure the API returns, via `.from_entity()`.

The DTO field names use **camelCase** (matching the JSON payload the Angular frontend sends), while the domain entity fields use **snake_case** (Python convention). The DTO methods perform the mapping between the two naming conventions.

| File | Inbound | Outbound |
|---|---|---|
| [`person_dto.py`](app/application/dtos/person_dto.py) | `CreatePersonDTO` | `PersonResponseDTO` |
| [`product_dto.py`](app/application/dtos/product_dto.py) | `CreateProductDTO` | `ProductResponseDTO` |

### Infrastructure Layer — `app/infrastructure/`

Contains the *secondary adapters* — the concrete implementations of the domain repository ports.

| File | Implements |
|---|---|
| [`in_memory_person_repository.py`](app/infrastructure/repositories/in_memory_person_repository.py) | `PersonRepository` using a `dict[int, Person]` + `threading.Lock` |
| [`in_memory_product_repository.py`](app/infrastructure/repositories/in_memory_product_repository.py) | `ProductRepository` using the same pattern |

Both repositories are thread-safe (the ASGI server may handle concurrent requests) and assign auto-incrementing integer ids.

### Exposition Layer — `app/exposition/`

Contains the *primary adapter* — the FastAPI HTTP interface that drives the application.

| File | Role |
|---|---|
| [`dependencies.py`](app/exposition/dependencies.py) | Creates the repository singletons once at startup and exposes them as FastAPI `Depends()` callables |
| [`routers/persons_router.py`](app/exposition/routers/persons_router.py) | `GET /persons`, `POST /persons`, `DELETE /persons/{id}` |
| [`routers/products_router.py`](app/exposition/routers/products_router.py) | `GET /products`, `POST /products`, `DELETE /products/{id}` |

---

## Project structure

```
backend/
├── main.py                               FastAPI app — CORS + router registration
├── requirements.txt                      Runtime dependencies
├── pyproject.toml                        Project metadata + optional dev deps
│
└── app/
    │
    ├── domain/                           ── Core: no framework imports ──
    │   ├── entities/
    │   │   ├── person.py                 Person dataclass + PersonRole enum
    │   │   └── product.py               Product dataclass + ProductCategory enum
    │   └── repositories/
    │       ├── person_repository.py      Abstract port (ABC) for person CRUD
    │       └── product_repository.py     Abstract port (ABC) for product CRUD
    │
    ├── application/                      ── Business logic ──
    │   ├── dtos/
    │   │   ├── person_dto.py             CreatePersonDTO + PersonResponseDTO
    │   │   └── product_dto.py            CreateProductDTO + ProductResponseDTO
    │   └── use_cases/
    │       ├── person/
    │       │   ├── get_all_persons.py
    │       │   ├── create_person.py
    │       │   └── delete_person.py
    │       └── product/
    │           ├── get_all_products.py
    │           ├── create_product.py
    │           └── delete_product.py
    │
    ├── infrastructure/                   ── Secondary adapters ──
    │   └── repositories/
    │       ├── in_memory_person_repository.py
    │       └── in_memory_product_repository.py
    │
    └── exposition/                       ── Primary adapter ──
        ├── dependencies.py               DI wiring (singleton repositories)
        └── routers/
            ├── persons_router.py         /persons endpoints
            └── products_router.py        /products endpoints
```

---

## Request flow through the layers

A `POST /persons` request travels inward through the layers and back out:

```
HTTP POST /persons  {firstName: "Alice", ...}
    │
    ▼  Exposition Layer
    FastAPI deserialises body into CreatePersonDTO
    Pydantic validates all field constraints
    (returns 422 if validation fails)
    │
    ▼  Application Layer
    CreatePerson use case receives Person entity
    (converted from DTO via .to_entity())
    │
    ▼  Domain Layer
    PersonRepository.save(person) called on the port
    │
    ▼  Infrastructure Layer
    InMemoryPersonRepository assigns an id and stores the entity
    │
    ▲  back through Application → Exposition
    PersonResponseDTO.from_entity(person) shapes the response
    │
    HTTP 201  {"id": 1, "firstName": "Alice", ...}
```

---

## API reference

Full interactive documentation is available at `http://localhost:8000/docs`.

### Persons — `GET /persons`

Return all persons. Responds with `[]` when empty.

### Persons — `POST /persons`

Create a new person. The request body is validated against the constraints below.

| Field | Type | Required | Constraints |
|---|---|---|---|
| `firstName` | string | yes | 2–50 characters |
| `lastName` | string | yes | 2–50 characters |
| `nickname` | string | yes | 2–50 characters |
| `email` | string | yes | valid email address |
| `role` | string | yes | one of `admin`, `user`, `manager`, `guest` |
| `birthDate` | date | no | ISO 8601 date (`YYYY-MM-DD`) |
| `age` | integer | no | 0–150 |
| `bio` | string | no | max 500 characters |
| `isActive` | boolean | no | defaults to `true` |

**Response codes**

| Code | Meaning |
|---|---|
| `201 Created` | Person created — body contains the new record with its `id` |
| `422 Unprocessable Entity` | Validation failure — body contains a structured error list |

**Example**

```bash
curl -X POST http://localhost:8000/persons \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Alice",
    "lastName":  "Smith",
    "nickname":  "ali",
    "email":     "alice@example.com",
    "role":      "admin"
  }'
```

### Persons — `DELETE /persons/{id}`

Delete a person by integer id.

| Code | Meaning |
|---|---|
| `204 No Content` | Deleted successfully |
| `404 Not Found` | No person with that id |

---

### Products — `GET /products`

Return all products. Responds with `[]` when empty.

### Products — `POST /products`

Create a new product.

| Field | Type | Required | Constraints |
|---|---|---|---|
| `name` | string | yes | 2–100 characters |
| `sku` | string | yes | uppercase letters, digits, and hyphens only (`^[A-Z0-9-]+$`) |
| `price` | number | yes | ≥ 0 |
| `quantity` | integer | yes | ≥ 0 |
| `category` | string | yes | one of `electronics`, `clothing`, `food`, `books`, `other` |
| `description` | string | no | max 1000 characters |
| `releaseDate` | date | no | ISO 8601 date (`YYYY-MM-DD`) |
| `inStock` | boolean | no | defaults to `true` |

**Example**

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name":     "Laptop Pro",
    "sku":      "LAPTOP-001",
    "price":    999.99,
    "quantity": 50,
    "category": "electronics"
  }'
```

### Products — `DELETE /products/{id}`

Delete a product by integer id. Same response codes as the person delete endpoint.

---

### Health check — `GET /health`

Returns `{"status": "ok"}`. Useful for readiness probes.

---

## Storage

All data is stored in **memory** (Python dictionaries), protected by a `threading.Lock` for concurrent-request safety. There is **no database and no file system persistence** — every server restart starts with empty collections.

This makes the backend zero-configuration for development: no database to install or migrate. To swap in a persistent backend (e.g. SQLite, PostgreSQL), implement the `PersonRepository` and `ProductRepository` abstract ports with a new adapter class and wire it in `dependencies.py`. No other layer needs to change.

---

## Development commands

Run from the `backend/` directory (with the venv activated) or use the Makefile targets from the repository root.

| Command | Description |
|---|---|
| `make install-backend` | Create `.venv` and install all dependencies |
| `make start-backend` | Start uvicorn with `--reload` on port 8000 |
| `make dev` | Start Angular frontend **and** FastAPI backend in parallel |
| `.venv/bin/uvicorn main:app --reload --port 8000` | Start the server directly |
