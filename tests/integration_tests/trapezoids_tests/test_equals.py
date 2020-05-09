from hypothesis import given

from tests.utils import (BoundPortedTrapezoidsPair,
                         equivalence)
from . import strategies


@given(strategies.trapezoids_pairs, strategies.trapezoids_pairs)
def test_basic(first_trapezoids_pair: BoundPortedTrapezoidsPair,
               second_trapezoids_pair: BoundPortedTrapezoidsPair) -> None:
    first_bound, first_ported = first_trapezoids_pair
    second_bound, second_ported = second_trapezoids_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
