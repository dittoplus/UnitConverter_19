"""Convert use case — orchestrates entity conversion for a parsed request."""

from __future__ import annotations

from dataclasses import dataclass

from boundary.input.parser import ConversionRequest
from entity.converter import ConversionResult, ConversionService
from entity.registry import UnitRegistry


@dataclass(frozen=True)
class ConvertUseCaseResult:
    """Bundle passed to formatters — source input plus all conversion rows."""

    unit: str
    value: float
    conversions: list[ConversionResult]


class ConvertUseCase:
    """Application entry for converting one value to every registered unit."""

    def __init__(self, registry: UnitRegistry) -> None:
        self._service = ConversionService(registry)

    def execute(self, request: ConversionRequest) -> ConvertUseCaseResult:
        return ConvertUseCaseResult(
            unit=request.unit,
            value=request.value,
            conversions=self._service.convert_all(request.value, request.unit),
        )
