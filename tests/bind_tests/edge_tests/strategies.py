from operator import ne
from typing import Tuple

from _seidel import (Edge,
                     Point)
from hypothesis import strategies

from tests.strategies import (floats,
                              to_pairs)
from tests.utils import pack

floats = floats
points = strategies.builds(Point, floats, floats)


def sort_points(points_pair: Tuple[Point, Point]) -> Tuple[Point, Point]:
    first, second = points_pair
    return (points_pair
            if second.is_right_of(first)
            else (second, first))


sorted_points = to_pairs(points).filter(pack(ne)).map(sort_points)
edges = sorted_points.map(pack(Edge))
