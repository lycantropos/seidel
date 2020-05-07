from typing import Tuple

from seidel.point import Point
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs)

coordinates_pairs = coordinates_strategies.flatmap(to_pairs)
points = coordinates_strategies.flatmap(coordinates_to_ported_points)
points_strategies = coordinates_strategies.map(coordinates_to_ported_points)


def sort_points(points_pair: Tuple[Point, Point]) -> Tuple[Point, Point]:
    first, second = points_pair
    return (points_pair
            if second.is_right_of(first)
            else (second, first))


sorted_points_pairs = points_strategies.flatmap(to_pairs).map(sort_points)
