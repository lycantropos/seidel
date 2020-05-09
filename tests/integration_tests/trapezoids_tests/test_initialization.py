from typing import Tuple

from hypothesis import given

from tests.utils import (BoundPortedEdgesPair,
                         BoundPortedPointsPair,
                         BoundTrapezoid,
                         PortedTrapezoid,
                         are_bound_ported_trapezoids_equal)
from . import strategies


@given(strategies.sorted_points_pairs_pairs, strategies.edges_pairs,
       strategies.edges_pairs)
def test_basic(endpoints_pairs_pair: Tuple[BoundPortedPointsPair,
                                           BoundPortedPointsPair],
               above_edges: BoundPortedEdgesPair,
               below_edges: BoundPortedEdgesPair) -> None:
    ((bound_left, ported_left),
     (bound_right, ported_right)) = endpoints_pairs_pair
    bound_above, ported_above = above_edges
    bound_below, ported_below = below_edges

    bound, ported = (BoundTrapezoid(bound_left, bound_right, bound_above,
                                    bound_below),
                     PortedTrapezoid(ported_left, ported_right, ported_above,
                                     ported_below))

    assert are_bound_ported_trapezoids_equal(bound, ported)
