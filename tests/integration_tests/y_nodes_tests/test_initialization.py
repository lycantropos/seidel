from hypothesis import given

from tests.utils import (BoundPortedEdgesPair,
                         BoundPortedNodesPair,
                         BoundYNode,
                         PortedYNode,
                         are_bound_ported_y_nodes_equal)
from . import strategies


@given(strategies.edges_pairs, strategies.nodes_pairs, strategies.nodes_pairs)
def test_basic(edges_pair: BoundPortedEdgesPair,
               left_nodes: BoundPortedNodesPair,
               right_nodes: BoundPortedNodesPair) -> None:
    bound_edge, ported_edge = edges_pair
    bound_left, ported_left = left_nodes
    bound_right, ported_right = right_nodes

    bound, ported = (BoundYNode(bound_edge, bound_left, bound_right),
                     PortedYNode(ported_edge, ported_left, ported_right))

    assert are_bound_ported_y_nodes_equal(bound, ported)
