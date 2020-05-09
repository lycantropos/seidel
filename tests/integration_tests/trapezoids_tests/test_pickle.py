from hypothesis import given

from tests.utils import (BoundPortedTrapezoidsPair,
                         are_bound_ported_trapezoids_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.trapezoids_pairs)
def test_round_trip(trapezoids_pair: BoundPortedTrapezoidsPair) -> None:
    bound, ported = trapezoids_pair

    assert are_bound_ported_trapezoids_equal(pickle_round_trip(bound),
                                             pickle_round_trip(ported))
