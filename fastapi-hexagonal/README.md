## FastAPI Hexagonal Architecture Template

This template provides a FastAPI backend organized using Hexagonal Architecture (a.k.a. Ports and Adapters) as described by Alistair Cockburn. The code is split into four layers:

- Domain
- Application
- Infrastructure
- Exposition

### Run locally

1) Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Start the server:

```bash
uvicorn app.exposition.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for Swagger UI.

### Project layout

```
app/
  domain/                # Core entities and ports (pure business)
  application/           # Use cases (application services)
  infrastructure/        # Outbound adapters (DB, external systems)
  exposition/            # Inbound adapters (FastAPI, CLI, etc.)
```

### Notes

- The Exposition layer depends on Application, which depends on Domain.
- Infrastructure implements Domain ports and is wired into Exposition via simple dependency providers.
- The sample uses an in-memory repository for demonstration; swap it with a real adapter later.


