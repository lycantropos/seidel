from hypothesis import given

from tests.utils import (BoundPortedYNodesPair,
                         are_bound_ported_y_nodes_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.y_nodes_pairs)
def test_round_trip(y_nodes_pair: BoundPortedYNodesPair) -> None:
    bound, ported = y_nodes_pair

    assert are_bound_ported_y_nodes_equal(pickle_round_trip(bound),
                                          pickle_round_trip(ported))
