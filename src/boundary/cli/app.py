"""CLI application — thin shell over parser, validator, use case, and formatter."""

from __future__ import annotations

from collections.abc import Callable

from boundary.cli.constants import EXIT_FAILURE, EXIT_SUCCESS, INPUT_PROMPT
from boundary.cli.default_registry import build_default_registry
from boundary.input.parser import InputParser
from boundary.input.validator import InputValidator
from boundary.output.table_formatter import TableFormatter
from control.convert_use_case import ConvertUseCase


class CliApp:
    """Interactive CLI entry point — stdin/stdout only (FR-01, FR-02, NFR-02)."""

    def __init__(
        self,
        convert_use_case: ConvertUseCase,
        *,
        parser: InputParser | None = None,
        validator: InputValidator | None = None,
        formatter: TableFormatter | None = None,
    ) -> None:
        """Wire boundary collaborators for one convert flow.

        Args:
            convert_use_case: Application orchestrator backed by a unit registry.
            parser: Optional parser override (defaults to ``InputParser``).
            validator: Optional validator override (defaults to ``InputValidator``).
            formatter: Optional formatter override (defaults to ``TableFormatter``).
        """
        self._use_case: ConvertUseCase = convert_use_case
        self._parser: InputParser = parser or InputParser()
        self._validator: InputValidator = validator or InputValidator()
        self._formatter: TableFormatter = formatter or TableFormatter()

    @classmethod
    def create_default(cls) -> CliApp:
        """Build a CLI wired to the default ``config/units.json`` registry."""
        return cls(ConvertUseCase(build_default_registry()))

    def run_once(self, raw: str) -> list[str]:
        """Execute one convert request and return formatted table lines.

        Args:
            raw: User input in ``unit:value`` form.

        Returns:
            Table rows for every registered unit (BR-07 rounding in formatter).

        Raises:
            ValueError: When parsing or validation fails (PRD §8).
        """
        request = self._parser.parse_convert_input(raw)
        self._validator.validate_convert_request(request)
        result = self._use_case.execute(request)
        return self._formatter.format(result).lines

    def run(
        self,
        *,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
        prompt: str = INPUT_PROMPT,
    ) -> int:
        """Run one interactive convert cycle via injected I/O callables.

        Args:
            input_fn: Callable that reads one line of user input.
            output_fn: Callable that emits one output line or error message.
            prompt: Prompt shown before reading input.

        Returns:
            ``EXIT_SUCCESS`` on success, ``EXIT_FAILURE`` on user input errors.
        """
        try:
            raw = input_fn(prompt)
            for line in self.run_once(raw):
                output_fn(line)
            return EXIT_SUCCESS
        except ValueError as exc:
            output_fn(str(exc))
            return EXIT_FAILURE


def main() -> None:
    """Program entry point for ``UnitConverter.py`` and ``python -m boundary.cli``."""
    raise SystemExit(CliApp.create_default().run())
