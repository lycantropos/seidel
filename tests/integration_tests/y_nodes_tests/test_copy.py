import copy

from hypothesis import given

from tests.utils import (BoundPortedYNodesPair,
                         are_bound_ported_y_nodes_equal)
from . import strategies


@given(strategies.y_nodes_pairs)
def test_shallow(y_nodes_pair: BoundPortedYNodesPair) -> None:
    bound, ported = y_nodes_pair

    assert are_bound_ported_y_nodes_equal(copy.copy(bound),
                                          copy.copy(ported))


@given(strategies.y_nodes_pairs)
def test_deep(y_nodes_pair: BoundPortedYNodesPair) -> None:
    bound, ported = y_nodes_pair

    assert are_bound_ported_y_nodes_equal(copy.deepcopy(bound),
                                          copy.deepcopy(ported))
