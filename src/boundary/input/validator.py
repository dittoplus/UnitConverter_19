"""Validate parsed convert requests."""

from __future__ import annotations

from entity.models import ConversionRequest

from boundary.input.messages import ERR_NEGATIVE_MESSAGE


class InputValidator:
    """Enforces non-negative value policy (BR-06, NFR-03)."""

    def validate_convert_request(self, request: ConversionRequest) -> None:
        """Reject negative length values before conversion.

        Args:
            request: Parsed convert input from ``InputParser``.

        Raises:
            ValueError: When ``request.value`` is negative (ERR_NEGATIVE).
        """
        if request.value < 0:
            raise ValueError(ERR_NEGATIVE_MESSAGE)
