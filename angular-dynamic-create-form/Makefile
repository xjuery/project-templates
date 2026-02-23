# ============================================================
#  Angular Dynamic Create Form — Developer Makefile
# ============================================================
.DEFAULT_GOAL := help

FRONTEND_DIR  := frontend
MOCK_DIR      := mockserver
BACKEND_DIR   := backend

# Colours for terminal output
RESET  := \033[0m
BOLD   := \033[1m
GREEN  := \033[32m
YELLOW := \033[33m
CYAN   := \033[36m

# ── Help ─────────────────────────────────────────────────────
.PHONY: help
help: ## Show this help message
	@printf "\n$(BOLD)Usage:$(RESET)  make $(CYAN)<target>$(RESET)\n\n"
	@printf "$(BOLD)Targets:$(RESET)\n"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / \
		{printf "  $(CYAN)%-22s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf "\n$(BOLD)URLs:$(RESET)\n"
	@printf "  Frontend   → $(GREEN)http://localhost:4200$(RESET)\n"
	@printf "  Backend    → $(GREEN)http://localhost:8000$(RESET)\n"
	@printf "  API docs   → $(GREEN)http://localhost:8000/docs$(RESET)\n"
	@printf "  Mock API   → $(GREEN)http://localhost:3001$(RESET)\n\n"

# ── Installation ─────────────────────────────────────────────
.PHONY: install
install: install-frontend install-mock install-backend ## Install all dependencies

.PHONY: install-frontend
install-frontend: ## Install Angular frontend dependencies
	@printf "$(YELLOW)▶ Installing frontend dependencies...$(RESET)\n"
	@cd $(FRONTEND_DIR) && npm install
	@printf "$(GREEN)✔ Frontend dependencies installed$(RESET)\n"

.PHONY: install-mock
install-mock: ## Install mock server dependencies
	@printf "$(YELLOW)▶ Installing mock server dependencies...$(RESET)\n"
	@cd $(MOCK_DIR) && npm install
	@printf "$(GREEN)✔ Mock server dependencies installed$(RESET)\n"

.PHONY: install-backend
install-backend: ## Create Python venv and install FastAPI backend dependencies
	@printf "$(YELLOW)▶ Installing backend dependencies...$(RESET)\n"
	@cd $(BACKEND_DIR) && python3 -m venv .venv && .venv/bin/pip install --upgrade pip --quiet && .venv/bin/pip install -r requirements.txt --quiet
	@printf "$(GREEN)✔ Backend dependencies installed$(RESET)\n"

# ── Development ──────────────────────────────────────────────
.PHONY: dev
dev: ## Start frontend + backend in parallel (requires make 4.x with -j)
	@printf "$(YELLOW)▶ Starting development environment...$(RESET)\n"
	@printf "  Frontend → $(GREEN)http://localhost:4200$(RESET)\n"
	@printf "  Backend  → $(GREEN)http://localhost:8000$(RESET)\n\n"
	@$(MAKE) -j2 start-frontend start-backend

.PHONY: dev-mock
dev-mock: ## Start frontend + mock server in parallel (legacy)
	@printf "$(YELLOW)▶ Starting development environment (mock server)...$(RESET)\n"
	@printf "  Frontend → $(GREEN)http://localhost:4200$(RESET)\n"
	@printf "  Mock API → $(GREEN)http://localhost:3001$(RESET)\n\n"
	@$(MAKE) -j2 start-frontend-mock start-mock

.PHONY: start-frontend
start-frontend: ## Start the Angular dev server proxied to FastAPI backend (http://localhost:4200)
	@printf "$(YELLOW)▶ Starting Angular frontend (→ FastAPI backend)...$(RESET)\n"
	@cd $(FRONTEND_DIR) && npm start -- --proxy-config proxy.conf.backend.json

.PHONY: start-frontend-mock
start-frontend-mock: ## Start the Angular dev server proxied to the mock server (http://localhost:4200)
	@printf "$(YELLOW)▶ Starting Angular frontend (→ mock server)...$(RESET)\n"
	@cd $(FRONTEND_DIR) && npm start

.PHONY: start-backend
start-backend: ## Start the FastAPI backend (http://localhost:8000)
	@printf "$(YELLOW)▶ Starting FastAPI backend...$(RESET)\n"
	@cd $(BACKEND_DIR) && .venv/bin/uvicorn main:app --reload --port 8000

.PHONY: start-mock
start-mock: ## Start the json-server mock API (http://localhost:3001)
	@printf "$(YELLOW)▶ Starting mock API server...$(RESET)\n"
	@cd $(MOCK_DIR) && npm start

# ── Build ─────────────────────────────────────────────────────
.PHONY: build
build: ## Build the Angular app for production
	@printf "$(YELLOW)▶ Building frontend for production...$(RESET)\n"
	@cd $(FRONTEND_DIR) && npm run build
	@printf "$(GREEN)✔ Build complete — artifacts in $(FRONTEND_DIR)/dist/$(RESET)\n"

# ── Code quality ──────────────────────────────────────────────
.PHONY: lint
lint: ## Run the Angular linter
	@printf "$(YELLOW)▶ Running linter...$(RESET)\n"
	@cd $(FRONTEND_DIR) && npm run lint

.PHONY: format
format: ## Format code with Prettier (if configured)
	@printf "$(YELLOW)▶ Formatting code...$(RESET)\n"
	@cd $(FRONTEND_DIR) && npx prettier --write "src/**/*.{ts,html,scss}"

# ── Mock data ─────────────────────────────────────────────────
.PHONY: reset-data
reset-data: ## Reset mock database to empty state
	@printf "$(YELLOW)▶ Resetting mock database...$(RESET)\n"
	@echo '{"persons":[],"products":[]}' > $(MOCK_DIR)/db.json
	@printf "$(GREEN)✔ Mock database reset$(RESET)\n"

# ── Cleanup ───────────────────────────────────────────────────
.PHONY: clean
clean: ## Remove build artefacts
	@printf "$(YELLOW)▶ Removing build artefacts...$(RESET)\n"
	@rm -rf $(FRONTEND_DIR)/dist
	@printf "$(GREEN)✔ Clean complete$(RESET)\n"

.PHONY: clean-all
clean-all: ## Remove build artefacts, node_modules and backend venv (full reset)
	@printf "$(YELLOW)▶ Removing artefacts and dependencies...$(RESET)\n"
	@rm -rf $(FRONTEND_DIR)/dist $(FRONTEND_DIR)/node_modules $(MOCK_DIR)/node_modules $(BACKEND_DIR)/.venv
	@printf "$(GREEN)✔ Full clean complete — run 'make install' to reinstall$(RESET)\n"
