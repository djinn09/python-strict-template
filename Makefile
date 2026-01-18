.PHONY: setup install format lint typecheck security test quality clean help

# Default Python version
PYTHON := python3.12

# --- SETUP & MAINTENANCE ---
setup: ## Full project setup (install + hooks)
	uv run poe setup

install: ## Install dependencies
	uv run poe install

clean: ## Clean build artifacts
	uv run poe clean

# --- HYGIENE (Formatting & Linting) ---
format: ## Format code and fix issues
	uv run poe format

lint: ## Run linter (check only)
	uv run poe lint

# --- TYPE CHECKING ---
typecheck: ## Run all type checkers (BasedPyright + ty)
	uv run poe typecheck

# --- SECURITY ---
security: ## Run all security scans (Bandit + Semgrep + Audit)
	uv run poe security

# --- TESTING ---
test: ## Run tests with coverage
	uv run poe test

test-fast: ## Run tests without coverage
	uv run poe test-fast

# --- FULL QUALITY ASSURANCE ---
quality: ## Run FULL quality suite
	uv run poe quality

# --- HELP ---
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
