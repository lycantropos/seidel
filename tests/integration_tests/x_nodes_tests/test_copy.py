import copy

from hypothesis import given

from tests.utils import (BoundPortedXNodesPair,
                         are_bound_ported_x_nodes_equal)
from . import strategies


@given(strategies.x_nodes_pairs)
def test_shallow(x_nodes_pair: BoundPortedXNodesPair) -> None:
    bound, ported = x_nodes_pair

    assert are_bound_ported_x_nodes_equal(copy.copy(bound),
                                          copy.copy(ported))


@given(strategies.x_nodes_pairs)
def test_deep(x_nodes_pair: BoundPortedXNodesPair) -> None:
    bound, ported = x_nodes_pair

    assert are_bound_ported_x_nodes_equal(copy.deepcopy(bound),
                                          copy.deepcopy(ported))
