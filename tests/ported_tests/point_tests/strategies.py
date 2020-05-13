from typing import Tuple

from hypothesis import strategies

from seidel.hints import Coordinate
from seidel.point import Point
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs,
                              to_triplets)
from tests.utils import Strategy

coordinates_pairs = coordinates_strategies.flatmap(to_pairs)
points = coordinates_strategies.flatmap(coordinates_to_ported_points)


def coordinates_to_points_with_origins(coordinates: Strategy[Coordinate]
                                       ) -> Strategy[Tuple[Point, Point]]:
    return strategies.tuples(coordinates_to_ported_points(coordinates),
                             coordinates_to_origins(coordinates))


def coordinates_to_origins(coordinates: Strategy[Coordinate]
                           ) -> Strategy[Point]:
    def coordinate_to_origin(coordinate: Coordinate) -> Point:
        domain = type(coordinate)
        return Point(domain(), domain())

    return coordinates.map(coordinate_to_origin)


points_with_origins = (coordinates_strategies
                       .flatmap(coordinates_to_points_with_origins))


def coordinates_to_points_pairs_with_origins(coordinates: Strategy[Coordinate]
                                             ) -> Strategy[Tuple[Point, Point,
                                                                 Point]]:
    points = coordinates_to_ported_points(coordinates)
    return strategies.tuples(points, points,
                             coordinates_to_origins(coordinates))


points_pairs_with_origins = coordinates_strategies.flatmap(
        coordinates_to_points_pairs_with_origins)
points_strategies = coordinates_strategies.map(coordinates_to_ported_points)
points_pairs = points_strategies.flatmap(to_pairs)
points_triplets = points_strategies.flatmap(to_triplets)
