from hypothesis import given

from tests.utils import (BoundPortedNodesPair,
                         BoundPortedPointsPair,
                         are_bound_ported_nodes_equal)
from . import strategies


@given(strategies.nodes_pairs, strategies.points_pairs)
def test_basic(nodes_pair: BoundPortedNodesPair,
               points_pair: BoundPortedPointsPair) -> None:
    bound, ported = nodes_pair
    bound_point, ported_point = points_pair

    assert are_bound_ported_nodes_equal(bound.search_point(bound_point),
                                        ported.search_point(ported_point))
