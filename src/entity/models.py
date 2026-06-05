"""Immutable domain value objects shared across ECB layers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConversionRequest:
    """Parsed convert input — source unit name and non-negative length value."""

    unit: str
    value: float


@dataclass(frozen=True)
class ConversionResult:
    """Single conversion row — one target unit and its converted numeric value."""

    to_unit: str
    converted_value: float
