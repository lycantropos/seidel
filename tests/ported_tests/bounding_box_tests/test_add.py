from typing import Tuple

from hypothesis import given

from seidel.bounding_box import BoundingBox
from seidel.point import Point
from . import strategies


@given(strategies.bounding_boxes_with_points)
def test_basic(bounding_box_with_point: Tuple[BoundingBox, Point]) -> None:
    bounding_box, point = bounding_box_with_point

    result = bounding_box.add(point)

    assert result is None


@given(strategies.bounding_boxes_with_points)
def test_properties(bounding_box_with_point: Tuple[BoundingBox, Point]
                    ) -> None:
    bounding_box, point = bounding_box_with_point

    bounding_box.add(point)

    assert not bounding_box.empty
    assert not bounding_box.lower.is_right_of(point)
    assert not point.is_right_of(bounding_box.upper)
