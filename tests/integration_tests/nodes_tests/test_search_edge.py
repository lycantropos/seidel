from hypothesis import given

from tests.utils import (BoundPortedEdgesPair,
                         BoundPortedNodesPair,
                         are_bound_ported_trapezoids_equal)
from . import strategies


@given(strategies.nodes_pairs, strategies.edges_pairs)
def test_basic(nodes_pair: BoundPortedNodesPair,
               edges_pair: BoundPortedEdgesPair) -> None:
    bound, ported = nodes_pair
    bound_edge, ported_edge = edges_pair

    bound_result = bound.search_edge(bound_edge)
    ported_result = ported.search_edge(ported_edge)

    assert (bound_result is ported_result is None
            or are_bound_ported_trapezoids_equal(bound_result, ported_result))
