from typing import Tuple

from hypothesis import given

from seidel.hints import Coordinate
from seidel.point import Point
from . import strategies


@given(strategies.coordinates_pairs)
def test_basic(coordinates_pair: Tuple[Coordinate, Coordinate]) -> None:
    x, y = coordinates_pair

    result = Point(x, y)

    assert result.x == x
    assert result.y == y
