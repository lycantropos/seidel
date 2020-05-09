from _seidel import (Node,
                     Point,
                     XNode)
from hypothesis import given

from . import strategies


@given(strategies.points, strategies.nodes, strategies.nodes)
def test_basic(point: Point, left: Node, right: Node) -> None:
    result = XNode(point, left, right)

    assert result.point == point
    assert result.left == left
    assert result.right == right
