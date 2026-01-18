.PHONY: install sync lint format type-check test security audit check clean help

# Default Python version
PYTHON := python3.12

# =============================================================================
# Installation & Setup
# =============================================================================

install: ## Install dependencies and set up pre-commit hooks
	uv sync --all-extras
	uv run pre-commit install
	uv run pre-commit install --hook-type pre-push
	@echo "✅ Environment ready!"

sync: ## Sync dependencies
	uv sync --all-extras

# =============================================================================
# Code Quality
# =============================================================================

lint: ## Run linter (ruff)
	uv run ruff check src/ tests/

lint-fix: ## Run linter with auto-fix
	uv run ruff check src/ tests/ --fix

format: ## Format code (ruff format)
	uv run ruff format src/ tests/

format-check: ## Check formatting without modifying
	uv run ruff format --check src/ tests/

type-check: ## Run type checker (mypy)
	uv run mypy src/

# =============================================================================
# Testing
# =============================================================================

test: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

test-fast: ## Run tests without coverage
	uv run pytest

test-verbose: ## Run tests with verbose output
	uv run pytest -v --tb=long

test-html: ## Run tests and generate HTML coverage report
	uv run pytest --cov=src --cov-report=html
	@echo "📊 Coverage report: htmlcov/index.html"

# =============================================================================
# Security
# =============================================================================

security: ## Run all security checks
	@echo "🔐 Running Bandit..."
	uv run bandit -r src/ -c pyproject.toml
	@echo "📦 Running pip-audit..."
	uv run pip-audit
	@echo "✅ Security checks passed!"

bandit: ## Run Bandit security linter
	uv run bandit -r src/ -c pyproject.toml

audit: ## Audit dependencies for vulnerabilities
	uv run pip-audit

secrets-scan: ## Scan for secrets
	uv run detect-secrets scan --all-files --baseline .secrets.baseline

secrets-audit: ## Audit secrets baseline
	uv run detect-secrets audit .secrets.baseline

# =============================================================================
# Combined Checks
# =============================================================================

check: lint-fix format type-check test security ## Run all checks (CI simulation)
	@echo "✅ All checks passed!"

pre-commit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

# =============================================================================
# Utilities
# =============================================================================

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "🧹 Cleaned!"

# =============================================================================
# Help
# =============================================================================

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
