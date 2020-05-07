from typing import Tuple

from hypothesis import given

from seidel.point import Point
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.points)
def test_reflexivity(point: Point) -> None:
    assert point == point


@given(strategies.points_pairs)
def test_symmetry(points_pair: Tuple[Point, Point]) -> None:
    first_point, second_point = points_pair

    assert equivalence(first_point == second_point,
                       second_point == first_point)


@given(strategies.points_triplets)
def test_transitivity(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_point, second_point, third_point = points_triplet

    assert implication(first_point == second_point
                       and second_point == third_point,
                       first_point == third_point)


@given(strategies.points_pairs)
def test_connection_with_inequality(points_pair: Tuple[Point, Point]) -> None:
    first_point, second_point = points_pair

    assert equivalence(not first_point == second_point,
                       first_point != second_point)
