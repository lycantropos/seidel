from hypothesis import given

from tests.utils import (BoundPortedLeavesPair,
                         equivalence)
from . import strategies


@given(strategies.leaves_pairs, strategies.leaves_pairs)
def test_basic(first_leaves_pair: BoundPortedLeavesPair,
               second_leaves_pair: BoundPortedLeavesPair) -> None:
    first_bound, first_ported = first_leaves_pair
    second_bound, second_ported = second_leaves_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
