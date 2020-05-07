from typing import Tuple

from hypothesis import given

from seidel.bounding_box import BoundingBox
from seidel.point import Point
from . import strategies


@given(strategies.booleans, strategies.points_pairs)
def test_basic(empty: bool, points_pair: Tuple[Point, Point]) -> None:
    lower, upper = points_pair

    result = BoundingBox(empty, lower, upper)

    assert result.empty is empty
    assert result.lower == lower
    assert result.upper == upper
