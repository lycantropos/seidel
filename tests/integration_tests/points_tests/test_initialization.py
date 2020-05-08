from hypothesis import given

from tests.utils import (BoundPoint,
                         PortedPoint,
                         are_bound_ported_points_equal)
from . import strategies


@given(strategies.floats, strategies.floats)
def test_basic(x: float, y: float) -> None:
    bound, ported = BoundPoint(x, y), PortedPoint(x, y)

    assert are_bound_ported_points_equal(bound, ported)
