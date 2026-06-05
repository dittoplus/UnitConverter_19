"""Build the default unit registry from project configuration."""

from __future__ import annotations

import json
from pathlib import Path

from entity.registry import UnitRegistry

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_UNITS_CONFIG = _PROJECT_ROOT / "config" / "units.json"


def build_default_registry(config_path: Path | None = None) -> UnitRegistry:
    """Load unit factors from ``config/units.json`` (PRD §7.3, BR-05).

    Args:
        config_path: Optional override for tests or alternate deployments.

    Returns:
        Registry pre-populated with configured from_meter_factor entries.
    """
    path: Path = config_path or _DEFAULT_UNITS_CONFIG
    with path.open(encoding="utf-8") as handle:
        data: dict[str, object] = json.load(handle)

    units: dict[str, float] = {
        name: float(factor) for name, factor in dict(data["units"]).items()
    }
    registry = UnitRegistry()
    for unit, factor in units.items():
        registry.register(unit, factor)
    return registry
