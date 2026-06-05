"""UI/Boundary Track — input parsing, validation, output skeleton (U-IN / U-OUT).

SC-3: each test fails explicitly via ``pytest.fail`` until GREEN.
Boundary tests: real Entity injection where needed (SC-4); no unittest.mock.

C2C traceability:
  U-IN-01 → empty input (ERR_FORMAT, NFR-04)
  U-IN-02 → missing colon (ERR_FORMAT, NFR-04)
  U-IN-03 → negative value (ERR_NEGATIVE, NFR-03, BR-06)
  U-OUT-01 → valid meter:2.5 → all-unit output skeleton (FR-01, FR-02, FR-08 table)
"""

from __future__ import annotations

import re
from typing import Callable, Protocol

import pytest

# PRD §8 — user-facing messages (SSOT for boundary assertions)
ERR_FORMAT_MESSAGE = "Invalid format. Use unit:value (ex: meter:2.5)"
ERR_NEGATIVE_MESSAGE = "Value must be zero or positive"

DEFAULT_UNITS = ("meter", "feet", "yard")


class ConversionRequestExpect(Protocol):
    """GREEN ``boundary.input`` / shared DTO — parsed convert input.

    Attributes:
        unit: Source unit name (trimmed).
        value: Non-negative float length value.
    """

    unit: str
    value: float


class FormattedOutputExpect(Protocol):
    """GREEN table/CLI output bundle — one row per registered unit.

    Attributes:
        lines: Human-readable rows, e.g. ``2.5 meter = 8.2 feet`` (BR-07 rounding in formatter).
    """

    lines: list[str]


@pytest.fixture
def input_parser() -> Callable[[], object]:
    """Lazy factory for ``InputParser`` (no import during RED fixture setup)."""

    def _build():
        from boundary.input.parser import InputParser

        return InputParser()

    return _build


@pytest.fixture
def input_validator() -> Callable[[], object]:
    """Lazy factory for ``InputValidator`` (value/unit policy, NFR-03~05)."""

    def _build():
        from boundary.input.validator import InputValidator

        return InputValidator()

    return _build


@pytest.fixture
def table_formatter() -> Callable[[], object]:
    """Lazy factory for ``TableFormatter`` (FR-08 table skeleton)."""

    def _build():
        from boundary.output.table_formatter import TableFormatter

        return TableFormatter()

    return _build


@pytest.fixture
def convert_use_case() -> Callable[[], object]:
    """Lazy factory: ``ConvertUseCase`` with real ``UnitRegistry`` (3 default units)."""

    def _build():
        from control.convert_use_case import ConvertUseCase
        from entity.registry import UnitRegistry

        registry = UnitRegistry()
        registry.register("meter", 1.0)
        registry.register("feet", 3.28084)
        registry.register("yard", 1.09361)
        return ConvertUseCase(registry)

    return _build


def test_u_in_01_empty_string_raises_format_error(
    input_parser: Callable[[], object],
) -> None:
    pytest.fail("GREEN 구현 전 UI 트랙 RED 확인")
    parser = input_parser()

    with pytest.raises(ValueError) as exc_info:
        parser.parse_convert_input("")

    assert ERR_FORMAT_MESSAGE in str(exc_info.value)


test_u_in_01_empty_string_raises_format_error.__doc__ = """\
PRD ID: U-IN-01 | FR: FR-01 | NFR: NFR-04 | ERR: ERR_FORMAT

Given: empty raw input string.
When: InputParser.parse_convert_input is called.
Then: ValueError is raised and message contains ERR_FORMAT text.
"""


def test_u_in_02_missing_colon_raises_format_error_with_message(
    input_parser: Callable[[], object],
) -> None:
    pytest.fail("GREEN 구현 전 UI 트랙 RED 확인")
    parser = input_parser()

    with pytest.raises(ValueError) as exc_info:
        parser.parse_convert_input("meter")

    message = str(exc_info.value)
    assert ERR_FORMAT_MESSAGE in message
    assert "unit:value" in message
    assert "meter:2.5" in message


test_u_in_02_missing_colon_raises_format_error_with_message.__doc__ = """\
PRD ID: U-IN-02 | FR: FR-01 | NFR: NFR-04 | ERR: ERR_FORMAT

Given: raw input without colon separator (e.g. "meter").
When: InputParser.parse_convert_input is called.
Then: ValueError carries full ERR_FORMAT guidance for unit:value syntax.
"""


@pytest.mark.parametrize(
    "raw_input",
    [
        "meter:-1",
        "feet:-0.01",
        "yard:-999",
    ],
    ids=["meter_negative", "feet_fraction_negative", "yard_large_negative"],
)
def test_u_in_03_negative_value_rejected_by_validator(
    input_parser: Callable[[], object],
    input_validator: Callable[[], object],
    raw_input: str,
) -> None:
    pytest.fail("GREEN 구현 전 UI 트랙 RED 확인")
    parser = input_parser()
    validator = input_validator()

    request = parser.parse_convert_input(raw_input)
    assert request.value < 0

    with pytest.raises(ValueError) as exc_info:
        validator.validate_convert_request(request)

    assert ERR_NEGATIVE_MESSAGE in str(exc_info.value)


test_u_in_03_negative_value_rejected_by_validator.__doc__ = """\
PRD ID: U-IN-03 | FR: FR-10 | NFR: NFR-03 | BR: BR-06 | ERR: ERR_NEGATIVE

Given: syntactically valid unit:value with negative numeric value.
When: parser succeeds then InputValidator.validate_convert_request runs.
Then: ValueError is raised; system refuses conversion (no silent negative output).
"""


def test_u_out_01_valid_input_returns_all_unit_output_skeleton(
    input_parser: Callable[[], object],
    convert_use_case: Callable[[], object],
    table_formatter: Callable[[], object],
) -> None:
    pytest.fail("GREEN 구현 전 UI 트랙 RED 확인")
    parser = input_parser()
    use_case = convert_use_case()
    formatter = table_formatter()

    raw_input = "meter:2.5"
    request = parser.parse_convert_input(raw_input)

    assert request.unit == "meter"
    assert request.value == pytest.approx(2.5)

    results = use_case.execute(request)
    output: FormattedOutputExpect = formatter.format(results)

    assert len(output.lines) == len(DEFAULT_UNITS)

    line_pattern = re.compile(
        r"^\s*2\.5\s+meter\s*=\s*[\d.]+\s+(meter|feet|yard)\s*$"
    )
    target_units_found: set[str] = set()
    for line in output.lines:
        assert "=" in line
        assert "2.5" in line
        assert "meter" in line
        match = line_pattern.match(line)
        assert match is not None, f"line does not match output skeleton: {line!r}"
        target_units_found.add(match.group(1))

    assert target_units_found == set(DEFAULT_UNITS)


test_u_out_01_valid_input_returns_all_unit_output_skeleton.__doc__ = """\
PRD ID: U-OUT-01 | FR: FR-01, FR-02, FR-08 | NFR: NFR-02

Given: valid convert input "meter:2.5".
When: parse → ConvertUseCase.execute → TableFormatter.format.
Then: output.lines has one row per registered unit (meter, feet, yard)
      matching README table skeleton ``{value} {unit} = {converted} {target}``.
"""
