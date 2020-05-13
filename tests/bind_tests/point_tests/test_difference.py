from _seidel import Point
from hypothesis import given

from . import strategies


@given(strategies.points, strategies.points)
def test_basic(left: Point, right: Point) -> None:
    assert isinstance(left - right, Point)


@given(strategies.points, strategies.origins)
def test_right_neutral_element(point: Point, origin: Point) -> None:
    assert point - origin == point


@given(strategies.points, strategies.origins)
def test_self_inverse(point: Point, origin: Point) -> None:
    assert point - point == origin


@given(strategies.points, strategies.points, strategies.origins)
def test_equality_criteria(left: Point, right: Point, origin: Point) -> None:
    assert (left - right == origin) is (left == right)
