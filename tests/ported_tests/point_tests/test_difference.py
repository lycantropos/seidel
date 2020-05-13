from typing import Tuple

from hypothesis import given

from seidel.point import Point
from tests.utils import equivalence
from . import strategies


@given(strategies.points_pairs)
def test_basic(points_pair: Tuple[Point, Point]) -> None:
    left, right = points_pair

    assert isinstance(left - right, Point)


@given(strategies.points_with_origins)
def test_right_neutral_element(point_with_origin: Tuple[Point, Point]) -> None:
    point, origin = point_with_origin

    assert point - origin == point


@given(strategies.points_with_origins)
def test_self_inverse(point_with_origin: Tuple[Point, Point]) -> None:
    point, origin = point_with_origin

    assert point - point == origin


@given(strategies.points_pairs_with_origins)
def test_equality_criteria(points_pair_with_origin: Tuple[Point, Point, Point]
                           ) -> None:
    left, right, origin = points_pair_with_origin

    assert equivalence(left - right == origin, left == right)
