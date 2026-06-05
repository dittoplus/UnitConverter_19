"""Domain Logic Track — ConversionService (D-CNV-01~03).

SC-3: each test fails explicitly via ``pytest.fail`` until GREEN.
SC-4: no mocks — real ``UnitRegistry`` / ``ConversionService`` collaboration.

C2C traceability:
  D-CNV-01 → feet→meter (BR-01, BR-02, PRD §7.3)
  D-CNV-02 → meter→feet 5dp (BR-02, PRD §7.3)
  D-CNV-03 → feet→yard meter hub (BR-04, PRD §7.3)
"""

from __future__ import annotations

from typing import Callable, Protocol

import pytest

# config/units.json · PRD BR-02/03/05 (from_meter_factor: 1 meter = factor unit)
METER_FACTOR = 1.0
FEET_FACTOR = 3.28084
YARD_FACTOR = 1.09361

TOLERANCE_ABS = 1e-4
TOLERANCE_REL = 1e-4


class ConversionResultExpect(Protocol):
    """GREEN ``entity.models.ConversionResult`` contract (immutable value object).

    Attributes:
        to_unit: Target unit name registered in ``UnitRegistry``.
        converted_value: Value expressed in ``to_unit`` after hub conversion.
    """

    to_unit: str
    converted_value: float


def _converted(results: list[ConversionResultExpect], to_unit: str) -> float:
    """Extract ``converted_value`` for ``to_unit`` from ``convert_all`` results."""
    for result in results:
        if result.to_unit == to_unit:
            return result.converted_value
    raise AssertionError(f"no ConversionResult for to_unit={to_unit!r}")


@pytest.fixture
def sample_registry() -> Callable[[], object]:
    """Lazy factory: defers ``entity`` import until called (after ``pytest.fail`` in RED).

    Returns:
        Callable that builds a ``UnitRegistry`` with meter/feet/yard factors.
    """

    def _build():
        from entity.registry import UnitRegistry

        registry = UnitRegistry()
        registry.register("meter", METER_FACTOR)
        registry.register("feet", FEET_FACTOR)
        registry.register("yard", YARD_FACTOR)
        return registry

    return _build


def test_d_cnv_01_one_feet_to_meter_within_tolerance(
    sample_registry: Callable[[], object],
) -> None:
    from entity.converter import ConversionService

    registry = sample_registry()
    service = ConversionService(registry)

    source_value = 1.0
    from_unit = "feet"
    expected_meter = 0.3048

    results = service.convert_all(source_value, from_unit)

    assert _converted(results, "meter") == pytest.approx(
        expected_meter, abs=TOLERANCE_ABS
    )


test_d_cnv_01_one_feet_to_meter_within_tolerance.__doc__ = """\
PRD ID: D-CNV-01 | FR: FR-04 | 비즈니스 규칙: BR-01, BR-02

Given: 1.0 feet on a registry with from_meter_factor feet=3.28084.
When: ConversionService.convert_all is invoked.
Then: meter result is 0.3048 within absolute tolerance (1 / 3.28084).
"""


def test_d_cnv_02_convert_all_meter_to_feet_five_decimal_places(
    sample_registry: Callable[[], object],
) -> None:
    from entity.converter import ConversionService

    registry = sample_registry()
    service = ConversionService(registry)

    source_value = 2.5
    from_unit = "meter"
    expected_feet = 8.20210

    results = service.convert_all(source_value, from_unit)

    actual_feet = _converted(results, "feet")
    assert round(actual_feet, 5) == expected_feet


test_d_cnv_02_convert_all_meter_to_feet_five_decimal_places.__doc__ = """\
PRD ID: D-CNV-02 | FR: FR-04 | 비즈니스 규칙: BR-02

Given: 2.5 meter (domain full precision).
When: convert_all targets feet via from_meter_factor.
Then: feet equals 8.20210 when rounded to 5 decimal places (2.5 × 3.28084).
"""


def test_d_cnv_03_feet_to_yard_matches_meter_hub_path(
    sample_registry: Callable[[], object],
) -> None:
    from entity.converter import ConversionService

    registry = sample_registry()
    service = ConversionService(registry)

    source_value = 3.0
    from_unit = "feet"

    results = service.convert_all(source_value, from_unit)
    via_convert_all = _converted(results, "yard")

    base_meters = registry.to_base(source_value, from_unit)
    expected_yard = registry.from_base(base_meters, "yard")
    assert via_convert_all == pytest.approx(expected_yard, rel=TOLERANCE_REL)


test_d_cnv_03_feet_to_yard_matches_meter_hub_path.__doc__ = """\
PRD ID: D-CNV-03 | FR: FR-04 | 비즈니스 규칙: BR-04

Given: 3.0 feet.
When: convert_all produces yard via meter hub.
Then: yard equals from_base(to_base(feet)) on the same registry (no direct ft→yd shortcut).
"""

