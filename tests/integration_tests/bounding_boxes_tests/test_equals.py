from hypothesis import given

from tests.utils import (BoundPortedBoundingBoxesPair,
                         equivalence)
from . import strategies


@given(strategies.bounding_boxes_pairs, strategies.bounding_boxes_pairs)
def test_basic(first_bounding_boxes_pair: BoundPortedBoundingBoxesPair,
               second_bounding_boxes_pair: BoundPortedBoundingBoxesPair
               ) -> None:
    first_bound, first_ported = first_bounding_boxes_pair
    second_bound, second_ported = second_bounding_boxes_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
