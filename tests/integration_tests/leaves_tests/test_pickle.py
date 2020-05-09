from hypothesis import given

from tests.utils import (BoundPortedLeavesPair,
                         are_bound_ported_leaves_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.leaves_pairs)
def test_round_trip(leaves_pair: BoundPortedLeavesPair) -> None:
    bound, ported = leaves_pair

    assert are_bound_ported_leaves_equal(pickle_round_trip(bound),
                                         pickle_round_trip(ported))
