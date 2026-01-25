#!/usr/bin/env python3
"""Cross-platform wrapper for jscpd clone detection."""

import logging
import shutil
import subprocess  # noqa: S404
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> int:
    """Run jscpd with cross-platform compatibility."""
    # Find jscpd executable (handles both Windows .cmd and Unix)
    jscpd_path = shutil.which("jscpd")

    if not jscpd_path:
        logger.error("Error: jscpd not found. Install with: npm install -g jscpd")
        return 1

    # Run jscpd with all arguments passed to this script
    args = [jscpd_path, *sys.argv[1:]] if sys.argv[1:] else [jscpd_path, "."]
    result = subprocess.run(args, check=False)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
