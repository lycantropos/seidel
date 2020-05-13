from hypothesis import given

from tests.utils import (BoundPortedBoundingBoxesPair,
                         BoundPortedPointsPair,
                         are_bound_ported_bounding_boxes_equal)
from . import strategies


@given(strategies.bounding_boxes_pairs, strategies.points_pairs)
def test_basic(bounding_boxes_pair: BoundPortedBoundingBoxesPair,
               points_pair: BoundPortedPointsPair) -> None:
    bound, ported = bounding_boxes_pair
    bound_point, ported_point = points_pair

    bound.add(bound_point)
    ported.add(ported_point)

    assert are_bound_ported_bounding_boxes_equal(bound, ported)
