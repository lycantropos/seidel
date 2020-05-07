from typing import Tuple

from hypothesis import given

from seidel.edge import Edge
from seidel.point import Point
from . import strategies


@given(strategies.sorted_points_pairs)
def test_basic(endpoints: Tuple[Point, Point]) -> None:
    left, right = endpoints

    result = Edge(left, right)

    assert result.left == left
    assert result.right == right
