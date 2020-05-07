from typing import Tuple

from hypothesis import given

from seidel.point import Point
from tests.utils import implication
from . import strategies


@given(strategies.points_pairs)
def test_basic(points_pair: Tuple[Point, Point]) -> None:
    first_point, second_point = points_pair

    result = first_point.is_right_of(second_point)

    assert isinstance(result, bool)


@given(strategies.points)
def test_irreflexivity(point: Point) -> None:
    assert not point.is_right_of(point)


@given(strategies.points_pairs)
def test_asymmetry(points_pair: Tuple[Point, Point]) -> None:
    first_point, second_point = points_pair

    assert implication(first_point.is_right_of(second_point),
                       not second_point.is_right_of(first_point))


@given(strategies.points_triplets)
def test_transitivity(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_point, second_point, third_point = points_triplet

    assert implication(first_point.is_right_of(second_point)
                       and second_point.is_right_of(third_point),
                       first_point.is_right_of(third_point))
