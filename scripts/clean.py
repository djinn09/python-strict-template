"""Cross-platform script to clean build artifacts and temporary files."""

import shutil
from pathlib import Path

for pattern in [
    "build",
    "dist",
    "*.egg-info",
    ".pytest_cache",
    ".ruff_cache",
    "htmlcov",
]:
    for path in Path().glob(pattern):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)

# Also explicitly remove .coverage if it exists but wasn't caught by glob
coverage_file = Path(".coverage")
if coverage_file.exists():
    coverage_file.unlink(missing_ok=True)
