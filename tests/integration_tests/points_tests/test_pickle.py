from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         are_bound_ported_points_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.points_pairs)
def test_round_trip(points_pair: BoundPortedPointsPair) -> None:
    bound, ported = points_pair

    assert are_bound_ported_points_equal(pickle_round_trip(bound),
                                         pickle_round_trip(ported))
