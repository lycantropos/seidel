from _seidel import (BoundingBox,
                     Point)
from hypothesis import given

from . import strategies


@given(strategies.booleans, strategies.points, strategies.points)
def test_basic(empty: bool, lower: Point, upper: Point) -> None:
    result = BoundingBox(empty, lower, upper)

    assert result.empty is empty
    assert result.lower == lower
    assert result.upper == upper
