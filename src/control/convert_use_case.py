"""Convert use case — orchestrates entity conversion for a parsed request."""

from __future__ import annotations

from dataclasses import dataclass

from entity.converter import ConversionService
from entity.models import ConversionRequest, ConversionResult
from entity.registry import UnitRegistry


@dataclass(frozen=True)
class ConvertUseCaseResult:
    """Bundle passed to formatters — source input plus all conversion rows."""

    unit: str
    value: float
    conversions: list[ConversionResult]


class ConvertUseCase:
    """Application entry for converting one value to every registered unit (FR-02)."""

    def __init__(self, registry: UnitRegistry) -> None:
        """Wire entity services from a shared registry instance.

        Args:
            registry: Unit table shared with registration and conversion flows.
        """
        self._service: ConversionService = ConversionService(registry)

    def execute(self, request: ConversionRequest) -> ConvertUseCaseResult:
        """Run hub conversion for a validated parse result.

        Args:
            request: Parsed unit and value (validation is a boundary concern).

        Returns:
            Source fields plus one conversion row per registered unit.
        """
        return ConvertUseCaseResult(
            unit=request.unit,
            value=request.value,
            conversions=self._service.convert_all(request.value, request.unit),
        )
