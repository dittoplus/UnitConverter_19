"""Entity layer — pure domain models, registry, and conversion (no I/O)."""

from __future__ import annotations

from entity.constants import BASE_UNIT
from entity.converter import ConversionService
from entity.models import ConversionRequest, ConversionResult
from entity.registry import UnitRegistry

__all__ = [
    "BASE_UNIT",
    "ConversionRequest",
    "ConversionResult",
    "ConversionService",
    "UnitRegistry",
]
