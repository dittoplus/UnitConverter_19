"""Table-style CLI output formatter."""

from __future__ import annotations

from dataclasses import dataclass

from control.convert_use_case import ConvertUseCaseResult


@dataclass(frozen=True)
class FormattedOutput:
    """Human-readable table rows for one convert operation."""

    lines: list[str]


class TableFormatter:
    """Formats conversion results as ``{value} {unit} = {converted} {target}`` lines."""

    def format(self, results: ConvertUseCaseResult) -> FormattedOutput:
        lines = [
            f"{results.value} {results.unit} = {round(conv.converted_value, 1)} {conv.to_unit}"
            for conv in results.conversions
        ]
        return FormattedOutput(lines=lines)
