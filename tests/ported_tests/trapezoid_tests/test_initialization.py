from typing import Tuple

from hypothesis import given

from seidel.edge import Edge
from seidel.point import Point
from seidel.trapezoid import Trapezoid
from . import strategies


@given(strategies.points_pairs_edges_pairs)
def test_basic(points_pair_edges_pair: Tuple[Point, Point, Edge, Edge]
               ) -> None:
    left, right, below, above = points_pair_edges_pair

    result = Trapezoid(left, right, below, above)

    assert result.left == left
    assert result.right == right
    assert result.below == below
    assert result.above == above
