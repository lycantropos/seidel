from typing import Tuple

from hypothesis import strategies

from seidel.edge import Edge
from seidel.hints import Coordinate
from seidel.point import Point
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_edges,
                              coordinates_to_ported_points)
from tests.utils import Strategy


def coordinates_to_points_pairs_edges_pairs(coordinates: Strategy[Coordinate]
                                            ) -> Strategy[Tuple[Point, Point,
                                                                Edge, Edge]]:
    points = coordinates_to_ported_points(coordinates)
    edges = coordinates_to_ported_edges(coordinates)
    return strategies.tuples(points, points, edges, edges)


points_pairs_edges_pairs = (coordinates_strategies
                            .flatmap(coordinates_to_points_pairs_edges_pairs))
