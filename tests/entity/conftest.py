"""Per-test eviction so lazy imports resolve ``src/entity``."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SRC_STR = str(Path(__file__).resolve().parent.parent.parent / "src")
_TESTS_ENTITY = Path(__file__).resolve().parent


def _ensure_src_entity() -> None:
    if _SRC_STR in sys.path:
        sys.path.remove(_SRC_STR)
    sys.path.insert(0, _SRC_STR)

    for name in list(sys.modules):
        if name != "entity" and not name.startswith("entity."):
            continue
        mod = sys.modules[name]
        mod_file = getattr(mod, "__file__", None)
        if mod_file is None:
            continue
        if Path(mod_file).resolve().parent == _TESTS_ENTITY:
            del sys.modules[name]


@pytest.fixture(autouse=True)
def _domain_entity_package() -> None:
    _ensure_src_entity()
