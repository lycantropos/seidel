from hypothesis import given

from tests.utils import (BoundPortedEdgesPair,
                         BoundPortedPointsPair)
from . import strategies


@given(strategies.edges_pairs, strategies.points_pairs)
def test_round_trip(edges_pair: BoundPortedEdgesPair,
                    points_pair: BoundPortedPointsPair) -> None:
    bound, ported = edges_pair
    bound_point, ported_point = points_pair

    assert (bound.orientation_with(bound_point)
            == ported.orientation_with(ported_point))
