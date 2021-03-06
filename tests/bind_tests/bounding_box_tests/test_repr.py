import sys

from _seidel import BoundingBox
from hypothesis import given

from . import strategies


@given(strategies.bounding_boxes)
def test_basic(bounding_box: BoundingBox) -> None:
    result = repr(bounding_box)

    assert result.startswith(BoundingBox.__module__)
    assert BoundingBox.__qualname__ in result


@given(strategies.bounding_boxes)
def test_round_trip(bounding_box: BoundingBox) -> None:
    result = repr(bounding_box)

    assert eval(result, sys.modules) == bounding_box
