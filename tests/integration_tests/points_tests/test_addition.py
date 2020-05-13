from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         are_bound_ported_points_equal)
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs)
def test_basic(left_points_pair: BoundPortedPointsPair,
               right_points_pair: BoundPortedPointsPair) -> None:
    bound_left, ported_left = left_points_pair
    bound_right, ported_right = right_points_pair

    assert are_bound_ported_points_equal(bound_left + bound_right,
                                         ported_left + ported_right)
