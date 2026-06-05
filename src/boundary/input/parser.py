"""Parse ``unit:value`` convert input strings."""

from __future__ import annotations

from entity.models import ConversionRequest

from boundary.input.messages import ERR_FORMAT_MESSAGE

# Re-export for callers that historically imported the DTO from the parser module.
__all__ = ["ConversionRequest", "InputParser"]


class InputParser:
    """Parses raw CLI input into a ``ConversionRequest`` (FR-01)."""

    _UNIT_VALUE_SEPARATOR: str = ":"

    def parse_convert_input(self, raw: str) -> ConversionRequest:
        """Parse ``{unit}:{value}`` input into a structured request.

        Args:
            raw: Untrimmed user input (e.g. ``"meter:2.5"``).

        Returns:
            Parsed unit name (trimmed) and numeric value.

        Raises:
            ValueError: When format is invalid (ERR_FORMAT, NFR-04).
        """
        text: str = raw.strip()
        if not text or self._UNIT_VALUE_SEPARATOR not in text:
            raise ValueError(ERR_FORMAT_MESSAGE)

        unit_part, value_part = text.split(self._UNIT_VALUE_SEPARATOR, 1)
        unit: str = unit_part.strip()
        if not unit:
            raise ValueError(ERR_FORMAT_MESSAGE)

        try:
            value: float = float(value_part.strip())
        except ValueError:
            raise ValueError(ERR_FORMAT_MESSAGE)

        return ConversionRequest(unit=unit, value=value)
