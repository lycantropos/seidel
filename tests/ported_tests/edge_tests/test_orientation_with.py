from typing import Tuple

from hypothesis import given

from seidel.edge import Edge
from seidel.point import Point
from . import strategies


@given(strategies.edges_with_points)
def test_basic(edge_with_point: Tuple[Edge, Point]) -> None:
    edge, point = edge_with_point

    assert edge.orientation_with(point) in (-1, 0, 1)


@given(strategies.edges)
def test_endpoints(edge: Edge) -> None:
    assert edge.orientation_with(edge.left) == 0
    assert edge.orientation_with(edge.right) == 0
