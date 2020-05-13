from _seidel import Point
from hypothesis import given

from . import strategies


@given(strategies.points, strategies.points)
def test_basic(left: Point, right: Point) -> None:
    assert isinstance(left + right, Point)


@given(strategies.points, strategies.points)
def test_commutativity(left: Point, right: Point) -> None:
    assert left + right == right + left


@given(strategies.points, strategies.origins)
def test_left_neutral_element(point: Point, origin: Point) -> None:
    assert origin + point == point


@given(strategies.points, strategies.origins)
def test_right_neutral_element(point: Point, origin: Point) -> None:
    assert point + origin == point
