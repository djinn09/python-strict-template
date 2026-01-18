# Python Strict Template

A comprehensive Python project template with a **curated safety toolchain** for protecting LLM-generated code.

## Quick Start

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

## Toolchain

| Layer        | Tool                                                                                        | Purpose                                           |
| ------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Linting**  | [Ruff](https://docs.astral.sh/ruff/)                                                        | Ultra-fast linter + formatter (replaces 8+ tools) |
| **Types**    | [BasedPyright](https://docs.basedpyright.com/)                                              | Strict static type checking                       |
| **Security** | [Bandit](https://bandit.readthedocs.io/) + [pip-audit](https://pypi.org/project/pip-audit/) | Security analysis & CVE scanning                  |
| **Quality**  | [PyScn](https://github.com/j178/pyscn) + [Vulture](https://github.com/jendrikseipp/vulture) | Quality scan + Dead code detection                |
| **Testing**  | [Pytest](https://pytest.org/) + [Hypothesis](https://hypothesis.readthedocs.io/)            | Unit + property-based testing                     |
| **Runtime**  | [Pydantic](https://docs.pydantic.dev/) + [Beartype](https://beartype.readthedocs.io/)       | Data validation + type checking                   |
| **CI**       | [prek](https://github.com/j178/prek)                                                        | Rust-based pre-commit runner (faster)             |

## Available Commands

Use **Poe the Poet** (`poe`) for all tasks:

### Hygiene

poe format # Format code and fix linting issues
poe lint # Run linter (check only)

### Type Checking

poe typecheck # Run BasedPyright + ty

### Security & Testing

poe security # Run Bandit + Semgrep + Pip-Audit + Secrets
poe test # Run tests with coverage

### Full Suite

poe quality # Run EVERYTHING (The ultimate check)

# Cleanup

poe clean # Remove build artifacts

> **Tip**: Run `poe --help` to see all available tasks with descriptions.

## Project Structure

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

## Why This Toolchain?

LLM-generated code often has:

- [x] Type mismatches -> **Mypy + Beartype** catch them
- [x] Security vulnerabilities -> **Bandit + pip-audit** detect them
- [x] Edge case bugs -> **Hypothesis** finds them
- [x] Invalid data assumptions -> **Pydantic** validates at runtime
- [x] Hardcoded secrets -> **detect-secrets** blocks commits

This template turns:

```
Unsafe LLM Code → Verified, Typed, Secured Code
```

## Example Usage

### Pydantic Model Validation

```python
from src.example import User, UserRole

# [PASSED] Valid - works
user = User(id=1, name="Alice", email="alice@example.com")

# [FAILED] Invalid email - raises ValidationError immediately
user = User(id=1, name="Alice", email="not-an-email")
```

### Beartype Runtime Checking

```python
from src.example import calculate_sum

# [PASSED] Valid - works
calculate_sum([1, 2, 3])  # Returns 6.0

# [FAILED] Wrong type - raises BeartypeCallHintException
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
