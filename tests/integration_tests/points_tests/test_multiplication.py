from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         are_bound_ported_points_equal)
from . import strategies


@given(strategies.points_pairs, strategies.scales)
def test_basic(points_pair: BoundPortedPointsPair,
               scale: float) -> None:
    bound, ported = points_pair

    assert are_bound_ported_points_equal(bound * scale, ported * scale)
