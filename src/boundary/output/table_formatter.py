"""Table-style CLI output formatter."""

from __future__ import annotations

from dataclasses import dataclass

from control.convert_use_case import ConvertUseCaseResult

from boundary.output.constants import TABLE_DISPLAY_DECIMAL_PLACES


@dataclass(frozen=True)
class FormattedOutput:
    """Human-readable table rows for one convert operation."""

    lines: list[str]


class TableFormatter:
    """Formats conversion results as ``{value} {unit} = {converted} {target}`` lines."""

    _OUTPUT_TEMPLATE: str = "{value} {unit} = {converted} {target}"

    def format(self, results: ConvertUseCaseResult) -> FormattedOutput:
        """Render use-case output as table rows with BR-07 decimal rounding.

        Args:
            results: Bundle of source input and all conversion rows.

        Returns:
            One formatted line per registered target unit.
        """
        lines: list[str] = [
            self._OUTPUT_TEMPLATE.format(
                value=results.value,
                unit=results.unit,
                converted=round(conv.converted_value, TABLE_DISPLAY_DECIMAL_PLACES),
                target=conv.to_unit,
            )
            for conv in results.conversions
        ]
        return FormattedOutput(lines=lines)
