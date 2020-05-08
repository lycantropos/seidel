from _seidel import (Edge,
                     Point,
                     Trapezoid)
from hypothesis import given

from . import strategies


@given(strategies.points, strategies.points,
       strategies.edges, strategies.edges)
def test_basic(left: Point, right: Point, above: Edge, below: Edge) -> None:
    result = Trapezoid(left, right, above, below)

    assert result.left == left
    assert result.right == right
    assert result.above == above
    assert result.below == below
