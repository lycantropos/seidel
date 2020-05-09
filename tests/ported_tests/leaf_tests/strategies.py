from seidel.hints import Coordinate
from seidel.leaf import Leaf
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points_pairs_edges_pairs,
                              coordinates_to_ported_trapezoids,
                              to_pairs,
                              to_triplets)
from tests.utils import Strategy

points_pairs_edges_pairs = coordinates_strategies.flatmap(
        coordinates_to_ported_points_pairs_edges_pairs)
trapezoids = coordinates_strategies.flatmap(coordinates_to_ported_trapezoids)


def coordinates_to_leaves(coordinates: Strategy[Coordinate]) -> Strategy[Leaf]:
    return coordinates_to_ported_trapezoids(coordinates).map(Leaf)


leaves = coordinates_strategies.flatmap(coordinates_to_leaves)
leaves_strategies = coordinates_strategies.map(coordinates_to_leaves)
leaves_pairs = leaves_strategies.flatmap(to_pairs)
leaves_triplets = leaves_strategies.flatmap(to_triplets)
