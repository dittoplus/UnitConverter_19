"""Unit registry — from_meter_factor storage and meter-hub conversion."""

from __future__ import annotations

BASE_UNIT = "meter"


class UnitRegistry:
    """Registers length units by from_meter_factor (1 meter = factor × unit)."""

    def __init__(self) -> None:
        self._units: dict[str, float] = {}

    def register(self, unit: str, from_meter_factor: float) -> None:
        self._units[unit] = from_meter_factor

    def all_units(self) -> list[str]:
        return list(self._units.keys())

    def to_base(self, value: float, unit: str) -> float:
        if unit == BASE_UNIT:
            return value
        return value / self._units[unit]

    def from_base(self, base: float, unit: str) -> float:
        if unit == BASE_UNIT:
            return base
        return base * self._units[unit]
