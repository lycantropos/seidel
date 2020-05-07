from typing import Tuple

from _seidel import (Edge,
                     Point)
from hypothesis import given

from . import strategies


@given(strategies.sorted_points)
def test_basic(endpoints: Tuple[Point, Point]) -> None:
    left, right = endpoints

    result = Edge(left, right)

    assert result.left == left
    assert result.right == right
