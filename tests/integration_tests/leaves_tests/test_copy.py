import copy

from hypothesis import given

from tests.utils import (BoundPortedLeavesPair,
                         are_bound_ported_leaves_equal)
from . import strategies


@given(strategies.leaves_pairs)
def test_shallow(leaves_pair: BoundPortedLeavesPair) -> None:
    bound, ported = leaves_pair

    assert are_bound_ported_leaves_equal(copy.copy(bound), copy.copy(ported))


@given(strategies.leaves_pairs)
def test_deep(leaves_pair: BoundPortedLeavesPair) -> None:
    bound, ported = leaves_pair

    assert are_bound_ported_leaves_equal(copy.deepcopy(bound),
                                         copy.deepcopy(ported))
