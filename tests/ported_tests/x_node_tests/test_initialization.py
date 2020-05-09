from typing import Tuple

from hypothesis import given

from seidel.node import Node
from seidel.point import Point
from seidel.x_node import XNode
from . import strategies


@given(strategies.points_with_nodes_pairs)
def test_basic(point_with_nodes_pair: Tuple[Point, Node, Node]) -> None:
    point, left, right = point_with_nodes_pair

    result = XNode(point, left, right)

    assert result.point == point
    assert result.left == left
    assert result.right == right
