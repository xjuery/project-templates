# ============================================================
#  Angular Dynamic Create Form — Developer Makefile
# ============================================================
.DEFAULT_GOAL := help

FRONTEND_DIR  := frontend
MOCK_DIR      := mockserver

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
	@printf "  Mock API   → $(GREEN)http://localhost:3001$(RESET)\n\n"

# ── Installation ─────────────────────────────────────────────
.PHONY: install
install: install-frontend install-mock ## Install all dependencies

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

# ── Development ──────────────────────────────────────────────
.PHONY: dev
dev: ## Start both servers in parallel (requires make 4.x with -j)
	@printf "$(YELLOW)▶ Starting development environment...$(RESET)\n"
	@printf "  Frontend → $(GREEN)http://localhost:4200$(RESET)\n"
	@printf "  Mock API → $(GREEN)http://localhost:3001$(RESET)\n\n"
	@$(MAKE) -j2 start-frontend start-mock

.PHONY: start-frontend
start-frontend: ## Start the Angular dev server (http://localhost:4200)
	@printf "$(YELLOW)▶ Starting Angular frontend...$(RESET)\n"
	@cd $(FRONTEND_DIR) && npm start

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
clean-all: ## Remove build artefacts AND node_modules (full reset)
	@printf "$(YELLOW)▶ Removing artefacts and node_modules...$(RESET)\n"
	@rm -rf $(FRONTEND_DIR)/dist $(FRONTEND_DIR)/node_modules $(MOCK_DIR)/node_modules
	@printf "$(GREEN)✔ Full clean complete — run 'make install' to reinstall$(RESET)\n"
