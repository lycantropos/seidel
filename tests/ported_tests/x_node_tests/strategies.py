from typing import Tuple

from hypothesis import strategies

from seidel.hints import Coordinate
from seidel.node import Node
from seidel.point import Point
from seidel.x_node import XNode
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_leaves,
                              coordinates_to_ported_points)
from tests.utils import Strategy


def coordinates_to_nodes(coordinates: Strategy[Coordinate]) -> Strategy[Node]:
    points = coordinates_to_ported_points(coordinates)

    def expand(nodes: Strategy[Node]) -> Strategy[Node]:
        return strategies.builds(XNode, points, nodes, nodes)

    return strategies.recursive(coordinates_to_ported_leaves(coordinates),
                                expand)


def coordinates_to_points_with_nodes_pairs(coordinates: Strategy[Coordinate]
                                           ) -> Strategy[Tuple[Point, Node,
                                                               Node]]:
    nodes = coordinates_to_nodes(coordinates)
    return strategies.tuples(coordinates_to_ported_points(coordinates),
                             nodes, nodes)


points_with_nodes_pairs = (coordinates_strategies
                           .flatmap(coordinates_to_points_with_nodes_pairs))
