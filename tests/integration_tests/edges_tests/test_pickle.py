from hypothesis import given

from tests.utils import (BoundPortedEdgesPair,
                         are_bound_ported_edges_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.edges_pairs)
def test_round_trip(edges_pair: BoundPortedEdgesPair) -> None:
    bound, ported = edges_pair

    assert are_bound_ported_edges_equal(pickle_round_trip(bound),
                                        pickle_round_trip(ported))
