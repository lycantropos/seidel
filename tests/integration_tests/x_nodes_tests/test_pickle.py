from hypothesis import given

from tests.utils import (BoundPortedXNodesPair,
                         are_bound_ported_x_nodes_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.x_nodes_pairs)
def test_round_trip(x_nodes_pair: BoundPortedXNodesPair) -> None:
    bound, ported = x_nodes_pair

    assert are_bound_ported_x_nodes_equal(pickle_round_trip(bound),
                                          pickle_round_trip(ported))
