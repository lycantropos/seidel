from typing import Tuple

from hypothesis import given

from seidel.point import Point
from . import strategies


@given(strategies.points_pairs)
def test_basic(points_pair: Tuple[Point, Point]) -> None:
    left, right = points_pair

    assert isinstance(left + right, Point)


@given(strategies.points_pairs)
def test_commutativity(points_pair: Tuple[Point, Point]) -> None:
    left, right = points_pair

    assert left + right == right + left


@given(strategies.points_with_origins)
def test_left_neutral_element(point_with_origin: Tuple[Point, Point]) -> None:
    point, origin = point_with_origin

    assert origin + point == point


@given(strategies.points_with_origins)
def test_right_neutral_element(point_with_origin: Tuple[Point, Point]) -> None:
    point, origin = point_with_origin

    assert point + origin == point
