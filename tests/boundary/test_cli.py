"""Boundary Track — CLI thin shell (CLI-01~04).

C2C traceability:
  CLI-01 → run_once valid meter:2.5 → table lines (U-OUT-01, FR-01, FR-02)
  CLI-02 → run_once empty input → ERR_FORMAT (NFR-04)
  CLI-03 → run negative input → exit 1 + ERR_NEGATIVE (NFR-03)
  CLI-04 → run success → exit 0 and printed lines (FR-08 table)
"""

from __future__ import annotations

from typing import Callable

import pytest

ERR_FORMAT_MESSAGE = "Invalid format. Use unit:value (ex: meter:2.5)"
ERR_NEGATIVE_MESSAGE = "Value must be zero or positive"


@pytest.fixture
def cli_app() -> Callable[[], object]:
    """Lazy factory for ``CliApp`` with default registry from config/units.json."""

    def _build():
        from boundary.cli.app import CliApp

        return CliApp.create_default()

    return _build


def test_cli_01_run_once_valid_input_returns_table_lines(
    cli_app: Callable[[], object],
) -> None:
    app = cli_app()

    lines = app.run_once("meter:2.5")

    assert lines == [
        "2.5 meter = 2.5 meter",
        "2.5 meter = 8.2 feet",
        "2.5 meter = 2.7 yard",
    ]


def test_cli_02_run_once_invalid_format_raises(
    cli_app: Callable[[], object],
) -> None:
    app = cli_app()

    with pytest.raises(ValueError) as exc_info:
        app.run_once("")

    assert ERR_FORMAT_MESSAGE in str(exc_info.value)


def test_cli_03_run_negative_input_returns_non_zero_exit(
    cli_app: Callable[[], object],
) -> None:
    app = cli_app()
    outputs: list[str] = []

    code = app.run(
        input_fn=lambda _: "meter:-1",
        output_fn=outputs.append,
        prompt="",
    )

    assert code == 1
    assert any(ERR_NEGATIVE_MESSAGE in line for line in outputs)


def test_cli_04_run_success_returns_zero_exit(
    cli_app: Callable[[], object],
) -> None:
    app = cli_app()
    outputs: list[str] = []

    code = app.run(
        input_fn=lambda _: "meter:2.5",
        output_fn=outputs.append,
        prompt="",
    )

    assert code == 0
    assert outputs == [
        "2.5 meter = 2.5 meter",
        "2.5 meter = 8.2 feet",
        "2.5 meter = 2.7 yard",
    ]
