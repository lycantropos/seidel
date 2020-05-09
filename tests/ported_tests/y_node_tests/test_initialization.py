from typing import Tuple

from hypothesis import given

from seidel.edge import Edge
from seidel.node import Node
from seidel.y_node import YNode
from . import strategies


@given(strategies.edges_with_nodes_pairs)
def test_basic(edge_with_nodes_pair: Tuple[Edge, Node, Node]) -> None:
    point, above, below = edge_with_nodes_pair

    result = YNode(point, above, below)

    assert result.edge == point
    assert result.above == above
    assert result.below == below
