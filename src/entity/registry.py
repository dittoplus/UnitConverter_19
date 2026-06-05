"""Unit registry — from_meter_factor storage and meter-hub conversion."""

from __future__ import annotations

from entity.constants import BASE_UNIT


class UnitRegistry:
    """Registers length units by from_meter_factor (1 meter = factor × unit).

    Conversion follows PRD §7.3 hub API:
    ``to_base(value, unit) = value / factor`` (non-base),
    ``from_base(base, unit) = base * factor`` (non-base).
    """

    def __init__(self) -> None:
        """Initialize an empty in-memory unit table."""
        self._units: dict[str, float] = {}

    def register(self, unit: str, from_meter_factor: float) -> None:
        """Register or replace a unit with its from_meter_factor (BR-05).

        Args:
            unit: Unit name (e.g. ``"feet"``).
            from_meter_factor: How many ``unit`` equal one meter (``1 meter = factor unit``).
        """
        self._units[unit] = from_meter_factor

    def all_units(self) -> list[str]:
        """Return registered unit names in insertion order."""
        return list(self._units.keys())

    def to_base(self, value: float, unit: str) -> float:
        """Convert a value in ``unit`` to the base unit (meter).

        Args:
            value: Numeric length in ``unit``.
            unit: Source unit name registered in this registry.

        Returns:
            Equivalent value expressed in meters.
        """
        if unit == BASE_UNIT:
            return value
        return value / self._units[unit]

    def from_base(self, base: float, unit: str) -> float:
        """Convert a base-unit (meter) value into ``unit``.

        Args:
            base: Numeric length in meters.
            unit: Target unit name registered in this registry.

        Returns:
            Equivalent value expressed in ``unit``.
        """
        if unit == BASE_UNIT:
            return base
        return base * self._units[unit]
