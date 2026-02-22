# ──────────────────────────────────────────────────────────────────────────────
#  Angular Advanced Search — developer Makefile
#
#  Quick start:
#    make install      install all dependencies (frontend + backend)
#    make dev          run backend + frontend concurrently
#
#  For a cleaner experience open two separate terminals:
#    Terminal 1 → make backend-start
#    Terminal 2 → make frontend-start
# ──────────────────────────────────────────────────────────────────────────────

PYTHON  := python3
VENV    := backend/.venv
ACTIVATE := . $(VENV)/bin/activate

.DEFAULT_GOAL := help

# ── Help ──────────────────────────────────────────────────────────────────────

.PHONY: help
help:
	@printf "\033[1mAngular Advanced Search — development commands\033[0m\n\n"
	@printf "\033[4mAggregate\033[0m\n"
	@printf "  \033[36mmake install\033[0m           Install all dependencies (frontend + backend)\n"
	@printf "  \033[36mmake dev\033[0m               Run backend + frontend concurrently (output interleaved)\n"
	@printf "  \033[36mmake build\033[0m             Production build of the frontend\n"
	@printf "  \033[36mmake clean\033[0m             Remove build caches and output\n"
	@printf "  \033[36mmake clean-all\033[0m         Also remove node_modules and the Python venv\n"
	@printf "\n"
	@printf "\033[4mFrontend (Angular — port 4200)\033[0m\n"
	@printf "  \033[36mmake frontend-install\033[0m  npm install\n"
	@printf "  \033[36mmake frontend-start\033[0m    ng serve (dev server with live reload)\n"
	@printf "  \033[36mmake frontend-build\033[0m    ng build (production)\n"
	@printf "  \033[36mmake frontend-watch\033[0m    ng build --watch (rebuild on change)\n"
	@printf "  \033[36mmake frontend-test\033[0m     Karma/Jasmine unit tests\n"
	@printf "\n"
	@printf "\033[4mBackend (FastAPI — port 8000)\033[0m\n"
	@printf "  \033[36mmake backend-setup\033[0m     Create .venv and pip install\n"
	@printf "  \033[36mmake backend-install\033[0m   pip install into existing venv\n"
	@printf "  \033[36mmake backend-start\033[0m     uvicorn --reload (dev server)\n"
	@printf "  \033[36mmake backend-check\033[0m     Syntax-check all Python source files\n"
	@printf "\n"
	@printf "Docs: http://localhost:8000/docs after backend-start\n"

# ── Aggregate targets ─────────────────────────────────────────────────────────

.PHONY: install dev build clean clean-all

install: frontend-install backend-setup

## Run both servers in parallel. Ctrl-C stops both.
dev:
	$(MAKE) -j2 backend-start frontend-start

build: frontend-build

clean:
	rm -rf frontend/dist frontend/.angular
	find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find backend -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean
	rm -rf frontend/node_modules frontend/package-lock.json
	rm -rf $(VENV)

# ── Frontend ──────────────────────────────────────────────────────────────────

.PHONY: frontend-install frontend-start frontend-build frontend-watch frontend-test

frontend-install:
	cd frontend && npm install

frontend-start:
	cd frontend && npm start

frontend-build:
	cd frontend && npm run build

frontend-watch:
	cd frontend && npm run watch

frontend-test:
	cd frontend && npm test

# ── Backend ───────────────────────────────────────────────────────────────────

.PHONY: backend-setup backend-install backend-start backend-check

## Create the virtual environment if it doesn't exist, then install deps.
$(VENV):
	$(PYTHON) -m venv $(VENV)

backend-setup: $(VENV)
	$(ACTIVATE) && pip install --upgrade pip && pip install -r backend/requirements.txt

## (Re)install Python deps into the existing venv (faster than full setup).
backend-install:
	$(ACTIVATE) && pip install -r backend/requirements.txt

## Start the FastAPI server with hot-reload.
backend-start:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000

## Syntax-check all backend Python files without starting the server.
backend-check:
	find backend/app -name "*.py" | xargs $(PYTHON) -m py_compile && echo "All Python files: syntax OK"
