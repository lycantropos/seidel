from _seidel import (Edge,
                     Node,
                     YNode)
from hypothesis import given

from . import strategies


@given(strategies.edges, strategies.nodes, strategies.nodes)
def test_basic(edge: Edge, below: Node, above: Node) -> None:
    result = YNode(edge, below, above)

    assert result.edge == edge
    assert result.below == below
    assert result.above == above
