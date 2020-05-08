from hypothesis import given

from tests.utils import (BoundPortedBoundingBoxesPair,
                         are_bound_ported_bounding_boxes_equal,
                         pickle_round_trip)
from . import strategies


@given(strategies.bounding_boxes_pairs)
def test_round_trip(bounding_boxes_pair: BoundPortedBoundingBoxesPair) -> None:
    bound, ported = bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(pickle_round_trip(bound),
                                                 pickle_round_trip(ported))
