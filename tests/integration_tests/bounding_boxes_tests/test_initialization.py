from hypothesis import given

from tests.utils import (BoundBoundingBox,
                         BoundPoint,
                         PortedBoundingBox,
                         PortedPoint,
                         are_bound_ported_bounding_boxes_equal)
from . import strategies


@given(strategies.booleans, strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_basic(empty: bool,
               lower_x: float,
               lower_y: float,
               upper_x: float,
               upper_y: float
               ) -> None:
    bound, ported = (BoundBoundingBox(empty, BoundPoint(lower_x, lower_y),
                                      BoundPoint(upper_x, upper_y)),
                     PortedBoundingBox(empty, PortedPoint(lower_x, lower_y),
                                       PortedPoint(upper_x, upper_y)))

    assert are_bound_ported_bounding_boxes_equal(bound, ported)
