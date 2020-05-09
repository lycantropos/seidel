from hypothesis import given

from tests.utils import (BoundPortedNodesPair,
                         BoundPortedPointsPair,
                         BoundXNode,
                         PortedXNode,
                         are_bound_ported_x_nodes_equal)
from . import strategies


@given(strategies.points_pairs, strategies.nodes_pairs, strategies.nodes_pairs)
def test_basic(points_pair: BoundPortedPointsPair,
               left_nodes: BoundPortedNodesPair,
               right_nodes: BoundPortedNodesPair) -> None:
    bound_point, ported_point = points_pair
    bound_left, ported_left = left_nodes
    bound_right, ported_right = right_nodes

    bound, ported = (BoundXNode(bound_point, bound_left, bound_right),
                     PortedXNode(ported_point, ported_left, ported_right))

    assert are_bound_ported_x_nodes_equal(bound, ported)
