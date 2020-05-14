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

    assert are_bound_ported_trapezoids_equal(bound.search_edge(bound_edge),
                                             ported.search_edge(ported_edge))
