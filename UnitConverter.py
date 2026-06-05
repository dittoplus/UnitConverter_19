"""Legacy entry point — delegates to ECB CLI (R-05)."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from boundary.cli.app import main  # noqa: E402

if __name__ == "__main__":
    main()
