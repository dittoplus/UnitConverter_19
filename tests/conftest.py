"""Ensure ``src/entity`` wins over the homonymous ``tests/entity`` test package."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
_SRC_STR = str(_SRC)


def _prepend_src_to_path() -> None:
    if _SRC_STR in sys.path:
        sys.path.remove(_SRC_STR)
    sys.path.insert(0, _SRC_STR)


def _evict_shadow_entity_modules() -> None:
    tests_entity = (Path(__file__).resolve().parent / "entity").as_posix()
    for name in list(sys.modules):
        if name != "entity" and not name.startswith("entity."):
            continue
        mod = sys.modules[name]
        mod_file = getattr(mod, "__file__", None)
        if mod_file is None:
            continue
        if Path(mod_file).resolve().parent.as_posix() == tests_entity:
            del sys.modules[name]


_prepend_src_to_path()
_evict_shadow_entity_modules()


def pytest_configure(config) -> None:
    _prepend_src_to_path()
    _evict_shadow_entity_modules()
