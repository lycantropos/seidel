from typing import Tuple

from hypothesis import strategies

from seidel.hints import Coordinate
from seidel.node import Node
from seidel.point import Point
from seidel.x_node import XNode
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_leaves,
                              coordinates_to_ported_points,
                              recursive,
                              to_pairs,
                              to_triplets)
from tests.utils import (Strategy,
                         pack)


def coordinates_to_nodes(coordinates: Strategy[Coordinate]) -> Strategy[Node]:
    points = coordinates_to_ported_points(coordinates)

    def expand(nodes: Strategy[Node]) -> Strategy[Node]:
        return strategies.builds(XNode, points, nodes, nodes)

    return recursive(coordinates_to_ported_leaves(coordinates), expand)


def coordinates_to_points_with_nodes_pairs(coordinates: Strategy[Coordinate]
                                           ) -> Strategy[Tuple[Point, Node,
                                                               Node]]:
    nodes = coordinates_to_nodes(coordinates)
    return strategies.tuples(coordinates_to_ported_points(coordinates),
                             nodes, nodes)


points_with_nodes_pairs = (coordinates_strategies
                           .flatmap(coordinates_to_points_with_nodes_pairs))


def coordinates_to_x_nodes(coordinates: Strategy[Coordinate]
                           ) -> Strategy[XNode]:
    return coordinates_to_points_with_nodes_pairs(coordinates).map(pack(XNode))


x_nodes = coordinates_strategies.flatmap(coordinates_to_x_nodes)
x_nodes_strategies = coordinates_strategies.map(coordinates_to_x_nodes)
x_nodes_pairs = x_nodes_strategies.flatmap(to_pairs)
x_nodes_triplets = x_nodes_strategies.flatmap(to_triplets)
