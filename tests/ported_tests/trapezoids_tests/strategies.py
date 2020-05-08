from operator import add
from typing import Tuple

from hypothesis import strategies

from seidel.edge import Edge
from seidel.hints import Coordinate
from seidel.point import Point
from seidel.trapezoid import Trapezoid
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_edges,
                              coordinates_to_sorted_ported_points_pairs,
                              to_pairs,
                              to_triplets)
from tests.utils import (Strategy,
                         pack)


def coordinates_to_points_pairs_edges_pairs(coordinates: Strategy[Coordinate]
                                            ) -> Strategy[Tuple[Point, Point,
                                                                Edge, Edge]]:
    edges = coordinates_to_ported_edges(coordinates)
    return (strategies.tuples(
            coordinates_to_sorted_ported_points_pairs(coordinates),
            strategies.tuples(edges, edges))
            .map(pack(add)))


points_pairs_edges_pairs = (coordinates_strategies
                            .flatmap(coordinates_to_points_pairs_edges_pairs))


def coordinates_to_trapezoids(coordinates: Strategy[Coordinate]
                              ) -> Strategy[Trapezoid]:
    return (coordinates_to_points_pairs_edges_pairs(coordinates)
            .map(pack(Trapezoid)))


trapezoids = coordinates_strategies.flatmap(coordinates_to_trapezoids)
trapezoids_strategies = coordinates_strategies.map(coordinates_to_trapezoids)
trapezoids_pairs = trapezoids_strategies.flatmap(to_pairs)
trapezoids_triplets = trapezoids_strategies.flatmap(to_triplets)
