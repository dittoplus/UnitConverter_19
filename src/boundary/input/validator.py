"""Validate parsed convert requests."""

from __future__ import annotations

from boundary.input.parser import ConversionRequest

ERR_NEGATIVE_MESSAGE = "Value must be zero or positive"


class InputValidator:
    """Enforces non-negative value policy (BR-06, NFR-03)."""

    def validate_convert_request(self, request: ConversionRequest) -> None:
        if request.value < 0:
            raise ValueError(ERR_NEGATIVE_MESSAGE)
