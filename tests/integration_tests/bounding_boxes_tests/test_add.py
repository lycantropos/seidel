from hypothesis import given

from tests.utils import (BoundPortedBoundingBoxesPair,
                         BoundPortedPointsListsPair,
                         are_bound_ported_bounding_boxes_equal)
from . import strategies


@given(strategies.bounding_boxes_pairs, strategies.points_lists_pairs)
def test_basic(bounding_boxes_pair: BoundPortedBoundingBoxesPair,
               points_pair: BoundPortedPointsListsPair) -> None:
    bound, ported = bounding_boxes_pair
    bound_points, ported_points = points_pair

    for bound_point, ported_point in zip(bound_points, ported_points):
        bound.add(bound_point)
        ported.add(ported_point)

    assert are_bound_ported_bounding_boxes_equal(bound, ported)
