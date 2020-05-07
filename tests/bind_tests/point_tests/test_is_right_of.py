from hypothesis import given

from seidel.point import Point
from tests.utils import implication
from . import strategies


@given(strategies.points, strategies.points)
def test_basic(first_point: Point, second_point: Point) -> None:
    result = first_point.is_right_of(second_point)

    assert isinstance(result, bool)


@given(strategies.points)
def test_irreflexivity(point: Point) -> None:
    assert not point.is_right_of(point)


@given(strategies.points, strategies.points)
def test_asymmetry(first_point: Point, second_point: Point) -> None:
    assert implication(first_point.is_right_of(second_point),
                       not second_point.is_right_of(first_point))


@given(strategies.points, strategies.points, strategies.points)
def test_transitivity(first_point: Point,
                      second_point: Point,
                      third_point: Point) -> None:
    assert implication(first_point.is_right_of(second_point)
                       and second_point.is_right_of(third_point),
                       first_point.is_right_of(third_point))
