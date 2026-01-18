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
uv run poe quality
```

## Toolchain

| Layer          | Tool                                                                                                 | Purpose                                           |
| -------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Hygiene**    | [Ruff](https://docs.astral.sh/ruff/)                                                                 | Ultra-fast linter + formatter (Google Docstrings) |
| **Types**      | [BasedPyright](https://docs.basedpyright.com/) + [ty](https://github.com/astral-sh/ty)               | God-Mode type checking                            |
| **Security**   | [Bandit](https://bandit.readthedocs.io/) + [Semgrep](https://semgrep.dev/)                           | Security analysis & Advanced rules                |
| **Monitoring** | [pip-audit](https://pypi.org/project/pip-audit/) + [Secrets](https://github.com/Yelp/detect-secrets) | CVE scanning & Secret detection                   |
| **Quality**    | [PyScn](https://github.com/j178/pyscn) + [Vulture](https://github.com/jendrikseipp/vulture)          | Quality scan + Dead code detection                |
| **Testing**    | [Pytest](https://pytest.org/) + [Hypothesis](https://hypothesis.readthedocs.io/)                     | Unit + property-based testing                     |
| **Runtime**    | [Pydantic](https://docs.pydantic.dev/) + [Beartype](https://beartype.readthedocs.io/)                | Data validation + type checking                   |

## Available Commands

Use **Poe the Poet** (`poe`) for all tasks:

### Hygiene & Formatting

- `poe format`: Formats code and fixes linting issues.
- `poe lint`: Checks code without modifying.

### Type Checking

- `poe typecheck`: Runs both BasedPyright and `ty`.

### Security & Compliance

- `poe security`: Runs Bandit, Semgrep (Local + Auto), Pip-Audit, and Secrets scan.
- `poe test`: Runs unit tests with coverage.

### Full Quality Assurance

- `poe quality`: The ultimate check. Runs hygiene, types, security, testing, and quality tools in sequence.

> **Tip**: Run `poe --help` to see all available tasks with detailed descriptions.

## Project Structure

```
python-strict-template/
├── .semgrep/             # Custom security & docstring rules
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

LLM-generated code often has common "slop" patterns that this toolchain is designed to catch:

- [x] **Type mismatches** -> BasedPyright God-Mode + Beartype catch them.
- [x] **Vague Docstrings** -> Ruff + Custom Semgrep rules enforce Google-style `Args:` and `Returns:`.
- [x] **Security vulnerabilities** -> Bandit + Semgrep detect them.
- [x] **Edge case bugs** -> Hypothesis finds them through property testing.
- [x] **Hardcoded secrets** -> detect-secrets blocks them before they reach Git.

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

## Requirements

- **Python 3.12+**
- **[UV](https://docs.astral.sh/uv/)**

## 📄 License

MIT
