from _seidel import BoundingBox
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.bounding_boxes)
def test_reflexivity(bounding_box: BoundingBox) -> None:
    assert bounding_box == bounding_box


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_symmetry(first_bounding_box: BoundingBox,
                  second_bounding_box: BoundingBox) -> None:
    assert equivalence(first_bounding_box == second_bounding_box,
                       second_bounding_box == first_bounding_box)


@given(strategies.bounding_boxes, strategies.bounding_boxes,
       strategies.bounding_boxes)
def test_transitivity(first_bounding_box: BoundingBox,
                      second_bounding_box: BoundingBox,
                      third_bounding_box: BoundingBox) -> None:
    assert implication(first_bounding_box == second_bounding_box
                       and second_bounding_box == third_bounding_box,
                       first_bounding_box == third_bounding_box)


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_connection_with_inequality(first_bounding_box: BoundingBox,
                                    second_bounding_box: BoundingBox) -> None:
    assert equivalence(not first_bounding_box == second_bounding_box,
                       first_bounding_box != second_bounding_box)
