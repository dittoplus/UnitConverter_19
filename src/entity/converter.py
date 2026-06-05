"""Conversion service — converts a value to all registered units via meter hub."""

from __future__ import annotations

from dataclasses import dataclass

from entity.registry import UnitRegistry


@dataclass(frozen=True)
class ConversionResult:
    """Immutable conversion result for one target unit."""

    to_unit: str
    converted_value: float


class ConversionService:
    """Converts a source value to every unit registered in the hub registry."""

    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert_all(self, value: float, from_unit: str) -> list[ConversionResult]:
        base = self._registry.to_base(value, from_unit)
        return [
            ConversionResult(
                to_unit=target,
                converted_value=self._registry.from_base(base, target),
            )
            for target in self._registry.all_units()
        ]
