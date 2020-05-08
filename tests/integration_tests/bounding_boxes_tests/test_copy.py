import copy

from hypothesis import given

from tests.utils import (BoundPortedBoundingBoxesPair,
                         are_bound_ported_bounding_boxes_equal)
from . import strategies


@given(strategies.bounding_boxes_pairs)
def test_shallow(bounding_boxes_pair: BoundPortedBoundingBoxesPair) -> None:
    bound, ported = bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(copy.copy(bound),
                                                 copy.copy(ported))


@given(strategies.bounding_boxes_pairs)
def test_deep(bounding_boxes_pair: BoundPortedBoundingBoxesPair) -> None:
    bound, ported = bounding_boxes_pair

    assert are_bound_ported_bounding_boxes_equal(copy.deepcopy(bound),
                                                 copy.deepcopy(ported))
