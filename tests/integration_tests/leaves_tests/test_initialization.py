from hypothesis import given

from tests.utils import (BoundLeaf,
                         BoundPortedTrapezoidsPair,
                         PortedLeaf,
                         are_bound_ported_leaves_equal)
from . import strategies


@given(strategies.trapezoids_pairs)
def test_basic(trapezoids_pair: BoundPortedTrapezoidsPair) -> None:
    bound_trapezoid, ported_trapezoid = trapezoids_pair

    bound, ported = BoundLeaf(bound_trapezoid), PortedLeaf(ported_trapezoid)

    assert are_bound_ported_leaves_equal(bound, ported)
