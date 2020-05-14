from _seidel import (Edge,
                     Point)
from hypothesis import given

from . import strategies


@given(strategies.edges, strategies.points)
def test_basic(edge: Edge, point: Point) -> None:
    assert edge.orientation_with(point) in (-1, 0, 1)


@given(strategies.edges)
def test_endpoints(edge: Edge) -> None:
    assert edge.orientation_with(edge.left) == 0
    assert edge.orientation_with(edge.right) == 0
