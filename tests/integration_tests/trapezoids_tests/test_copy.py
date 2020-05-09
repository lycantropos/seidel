import copy

from hypothesis import given

from tests.utils import (BoundPortedTrapezoidsPair,
                         are_bound_ported_trapezoids_equal)
from . import strategies


@given(strategies.trapezoids_pairs)
def test_shallow(trapezoids_pair: BoundPortedTrapezoidsPair) -> None:
    bound, ported = trapezoids_pair

    assert are_bound_ported_trapezoids_equal(copy.copy(bound),
                                             copy.copy(ported))


@given(strategies.trapezoids_pairs)
def test_deep(trapezoids_pair: BoundPortedTrapezoidsPair) -> None:
    bound, ported = trapezoids_pair

    assert are_bound_ported_trapezoids_equal(copy.deepcopy(bound),
                                             copy.deepcopy(ported))
