from typing import Tuple

from _seidel import (Edge,
                     Point,
                     Trapezoid)
from hypothesis import given

from . import strategies


@given(strategies.sorted_points_pairs, strategies.edges, strategies.edges)
def test_basic(endpoints: Tuple[Point, Point],
               above: Edge,
               below: Edge) -> None:
    left, right = endpoints

    result = Trapezoid(left, right, above, below)

    assert result.left == left
    assert result.right == right
    assert result.above == above
    assert result.below == below
