from typing import Tuple

from hypothesis import strategies

from seidel.edge import Edge
from seidel.hints import Coordinate
from seidel.point import Point
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs,
                              to_triplets)
from tests.utils import (Strategy,
                         pack,
                         point_to_coordinates,
                         sort_points)

coordinates_pairs = coordinates_strategies.flatmap(to_pairs)
points = coordinates_strategies.flatmap(coordinates_to_ported_points)


def coordinates_to_sorted_points_pairs(coordinates: Strategy[Coordinate]
                                       ) -> Strategy[Tuple[Point, Point]]:
    return (strategies.lists(coordinates_to_ported_points(coordinates),
                             min_size=2,
                             max_size=2,
                             unique_by=point_to_coordinates)
            .map(tuple)
            .map(sort_points))


sorted_points_pairs = (coordinates_strategies
                       .flatmap(coordinates_to_sorted_points_pairs))


def coordinates_to_edges(coordinates: Strategy[Coordinate]) -> Strategy[Edge]:
    return coordinates_to_sorted_points_pairs(coordinates).map(pack(Edge))


edges = coordinates_strategies.flatmap(coordinates_to_edges)
edges_strategies = coordinates_strategies.map(coordinates_to_edges)
edges_pairs = edges_strategies.flatmap(to_pairs)
edges_triplets = edges_strategies.flatmap(to_triplets)
