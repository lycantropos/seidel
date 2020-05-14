from typing import Tuple

from hypothesis import strategies

from seidel.edge import Edge
from seidel.hints import Coordinate
from seidel.point import Point
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_edges,
                              coordinates_to_ported_points,
                              coordinates_to_sorted_ported_points_pairs,
                              to_pairs,
                              to_triplets)
from tests.utils import Strategy

sorted_points_pairs = (coordinates_strategies
                       .flatmap(coordinates_to_sorted_ported_points_pairs))
edges = coordinates_strategies.flatmap(coordinates_to_ported_edges)


def coordinates_to_edges_with_points(coordinates: Strategy[Coordinate]
                                     ) -> Strategy[Tuple[Edge, Point]]:
    return strategies.tuples(coordinates_to_ported_edges(coordinates),
                             coordinates_to_ported_points(coordinates))


edges_with_points = (coordinates_strategies
                     .flatmap(coordinates_to_edges_with_points))
edges_strategies = coordinates_strategies.map(coordinates_to_ported_edges)
edges_pairs = edges_strategies.flatmap(to_pairs)
edges_triplets = edges_strategies.flatmap(to_triplets)
