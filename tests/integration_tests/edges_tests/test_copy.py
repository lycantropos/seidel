import copy

from hypothesis import given

from tests.utils import (BoundPortedEdgesPair,
                         are_bound_ported_edges_equal)
from . import strategies


@given(strategies.edges_pairs)
def test_shallow(edges_pair: BoundPortedEdgesPair) -> None:
    bound, ported = edges_pair

    assert are_bound_ported_edges_equal(copy.copy(bound), copy.copy(ported))


@given(strategies.edges_pairs)
def test_deep(edges_pair: BoundPortedEdgesPair) -> None:
    bound, ported = edges_pair

    assert are_bound_ported_edges_equal(copy.deepcopy(bound),
                                        copy.deepcopy(ported))
