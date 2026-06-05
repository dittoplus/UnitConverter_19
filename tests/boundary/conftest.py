"""Per-test eviction so lazy imports resolve ``src/`` packages over ``tests/`` shadows."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SRC_STR = str(Path(__file__).resolve().parent.parent.parent / "src")
_TESTS_DIR = Path(__file__).resolve().parent.parent
_SHADOW_DIRS: dict[str, Path] = {
    "entity": _TESTS_DIR / "entity",
    "boundary": _TESTS_DIR / "boundary",
}


def _ensure_src_packages() -> None:
    if _SRC_STR in sys.path:
        sys.path.remove(_SRC_STR)
    sys.path.insert(0, _SRC_STR)

    for prefix, shadow_dir in _SHADOW_DIRS.items():
        for name in list(sys.modules):
            if name != prefix and not name.startswith(f"{prefix}."):
                continue
            mod = sys.modules[name]
            mod_file = getattr(mod, "__file__", None)
            if mod_file is None:
                continue
            if Path(mod_file).resolve().parent == shadow_dir:
                del sys.modules[name]


@pytest.fixture(autouse=True)
def _src_packages() -> None:
    _ensure_src_packages()
