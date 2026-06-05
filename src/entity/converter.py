"""Conversion service — converts a value to all registered units via meter hub."""

from __future__ import annotations

from entity.models import ConversionResult
from entity.registry import UnitRegistry


class ConversionService:
    """Converts a source value to every unit registered in the hub registry.

    Uses ``UnitRegistry`` as the sole conversion collaborator (FR-04, BR-04).
    """

    def __init__(self, registry: UnitRegistry) -> None:
        """Bind a registry that supplies factors and unit enumeration.

        Args:
            registry: Hub registry with from_meter_factor data (BR-05).
        """
        self._registry: UnitRegistry = registry

    def convert_all(self, value: float, from_unit: str) -> list[ConversionResult]:
        """Convert ``value`` from ``from_unit`` into every registered target unit.

        Args:
            value: Source numeric length (domain full precision).
            from_unit: Source unit name registered in the bound registry.

        Returns:
            One ``ConversionResult`` per registered unit, in registry order.
        """
        base: float = self._registry.to_base(value, from_unit)
        return [
            ConversionResult(
                to_unit=target,
                converted_value=self._registry.from_base(base, target),
            )
            for target in self._registry.all_units()
        ]
