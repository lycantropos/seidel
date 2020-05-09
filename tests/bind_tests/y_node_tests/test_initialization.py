from _seidel import (Edge,
                     Node,
                     YNode)
from hypothesis import given

from . import strategies


@given(strategies.edges, strategies.nodes, strategies.nodes)
def test_basic(edge: Edge, above: Node, below: Node) -> None:
    result = YNode(edge, above, below)

    assert result.edge == edge
    assert result.above == above
    assert result.below == below
