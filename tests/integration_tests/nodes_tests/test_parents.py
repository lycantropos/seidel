from hypothesis import given

from tests.utils import (BoundPortedNodesPair,
                         are_bound_ported_nodes_sequences_equal)
from . import strategies


@given(strategies.nodes_pairs)
def test_round_trip(x_nodes_pair: BoundPortedNodesPair) -> None:
    bound, ported = x_nodes_pair

    assert are_bound_ported_nodes_sequences_equal(bound.parents,
                                                  ported.parents)
