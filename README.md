# Python Strict Template 🛡️

A comprehensive Python project template with a **curated safety toolchain** for protecting LLM-generated code.

## 🚀 Quick Start

```bash
# Clone and enter
git clone <repo-url>
cd python-strict-template

# Install everything (requires UV)
uv sync --all-extras
uv run prek install  # Install git hooks (Rust-based, fast!)

# Run all checks
uv run poe check
```

## 🧰 Toolchain

| Layer        | Tool                                                                                        | Purpose                                           |
| ------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Linting**  | [Ruff](https://docs.astral.sh/ruff/)                                                        | Ultra-fast linter + formatter (replaces 8+ tools) |
| **Types**    | [BasedPyright](https://docs.basedpyright.com/)                                              | Strict static type checking                       |
| **Security** | [Bandit](https://bandit.readthedocs.io/) + [pip-audit](https://pypi.org/project/pip-audit/) | Security analysis & CVE scanning                  |
| **Quality**  | [PyScn](https://github.com/j178/pyscn) + [Vulture](https://github.com/jendrikseipp/vulture) | Quality scan + Dead code detection                |
| **Testing**  | [Pytest](https://pytest.org/) + [Hypothesis](https://hypothesis.readthedocs.io/)            | Unit + property-based testing                     |
| **Runtime**  | [Pydantic](https://docs.pydantic.dev/) + [Beartype](https://beartype.readthedocs.io/)       | Data validation + type checking                   |
| **CI**       | [prek](https://github.com/j178/prek)                                                        | Rust-based pre-commit runner (faster)             |

## 📋 Available Commands

Use **Poe the Poet** (`poe`) for all tasks:

```bash
# Setup
poe setup         # Full project setup (install + pre-commit)

# Code Quality
poe lint          # Run ruff check
poe format        # Run ruff format
poe typecheck     # Run strict type checking (BasedPyright)

# Testing
poe test          # Run tests with coverage

# Security & Quality
poe security      # Run bandit, audit, dead-code, quality
poe dead-code     # Find unused code (vulture)
poe quality       # Run deep quality scan (pyscn)

# Combined
poe check         # Run ALL checks (CI simulation)
```

# Cleanup

poe clean # Remove build artifacts

> 💡 **Tip**: Run `poe --help` to see all available tasks with descriptions.

## 🏗️ Project Structure

```
python-strict-template/
├── src/
│   ├── __init__.py       # Package init
│   ├── py.typed          # PEP 561 typed marker
│   └── example.py        # Example with Pydantic + Beartype
├── tests/
│   ├── conftest.py       # Pytest fixtures
│   └── test_example.py   # Tests with Hypothesis
├── pyproject.toml        # All configs in one place
├── .pre-commit-config.yaml
├── Makefile
└── README.md
```

## 🔒 Why This Toolchain?

LLM-generated code often has:

- ❌ Type mismatches → **Mypy + Beartype** catch them
- ❌ Security vulnerabilities → **Bandit + pip-audit** detect them
- ❌ Edge case bugs → **Hypothesis** finds them
- ❌ Invalid data assumptions → **Pydantic** validates at runtime
- ❌ Hardcoded secrets → **detect-secrets** blocks commits

This template turns:

```
Unsafe LLM Code → Verified, Typed, Secured Code
```

## 🎯 Example Usage

### Pydantic Model Validation

```python
from src.example import User, UserRole

# ✅ Valid - works
user = User(id=1, name="Alice", email="alice@example.com")

# ❌ Invalid email - raises ValidationError immediately
user = User(id=1, name="Alice", email="not-an-email")
```

### Beartype Runtime Checking

```python
from src.example import calculate_sum

# ✅ Valid - works
calculate_sum([1, 2, 3])  # Returns 6.0

# ❌ Wrong type - raises BeartypeCallHintException
calculate_sum(["1", "2", "3"])  # LLMs often make this mistake!
```

### Hypothesis Property Testing

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sum_always_works(numbers):
    # Tests with 100s of random inputs!
    result = calculate_sum(numbers)
    assert result == sum(numbers)
```

## 📦 Requirements

- **Python 3.12+**
- **[UV](https://docs.astral.sh/uv/)** - Install with `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`

## 📄 License

MIT
