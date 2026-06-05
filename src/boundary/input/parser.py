"""Parse ``unit:value`` convert input strings."""

from __future__ import annotations

from dataclasses import dataclass

ERR_FORMAT_MESSAGE = "Invalid format. Use unit:value (ex: meter:2.5)"


@dataclass(frozen=True)
class ConversionRequest:
    """Parsed convert input — source unit and numeric value."""

    unit: str
    value: float


class InputParser:
    """Parses raw CLI input into a ``ConversionRequest``."""

    def parse_convert_input(self, raw: str) -> ConversionRequest:
        text = raw.strip()
        if not text or ":" not in text:
            raise ValueError(ERR_FORMAT_MESSAGE)

        unit_part, value_part = text.split(":", 1)
        unit = unit_part.strip()
        if not unit:
            raise ValueError(ERR_FORMAT_MESSAGE)

        try:
            value = float(value_part.strip())
        except ValueError:
            raise ValueError(ERR_FORMAT_MESSAGE)

        return ConversionRequest(unit=unit, value=value)
