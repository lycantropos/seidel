from functools import partial
from operator import add
from typing import Tuple

from hypothesis import strategies

from seidel.hints import Coordinate
from tests.utils import (BoundBoundingBox,
                         BoundEdge,
                         BoundLeaf,
                         BoundPoint,
                         BoundPortedBoundingBoxesPair,
                         BoundPortedEdgesPair,
                         BoundPortedLeavesPair,
                         BoundPortedNodesPair,
                         BoundPortedPointsPair,
                         BoundPortedTrapezoidsPair,
                         BoundPortedXNodesPair,
                         BoundPortedYNodesPair,
                         BoundTrapezoid,
                         BoundXNode,
                         BoundYNode,
                         Domain,
                         PortedBoundingBox,
                         PortedEdge,
                         PortedLeaf,
                         PortedNode,
                         PortedPoint,
                         PortedTrapezoid,
                         PortedXNode,
                         PortedYNode,
                         Strategy,
                         pack,
                         point_to_coordinates,
                         sort_points)


def coordinates_to_ported_edges(coordinates: Strategy[Coordinate]
                                ) -> Strategy[PortedEdge]:
    return (coordinates_to_sorted_ported_points_pairs(coordinates)
            .map(pack(PortedEdge)))


def coordinates_to_ported_leaves(coordinates: Strategy[Coordinate]
                                 ) -> Strategy[PortedLeaf]:
    return coordinates_to_ported_trapezoids(coordinates).map(PortedLeaf)


def coordinates_to_ported_nodes(coordinates: Strategy[Coordinate]
                                ) -> Strategy[PortedNode]:
    edges = coordinates_to_ported_edges(coordinates)
    points = coordinates_to_ported_points(coordinates)

    def expand(nodes: Strategy[PortedNode]) -> Strategy[PortedNode]:
        return (strategies.builds(PortedXNode, points, nodes, nodes)
                | strategies.builds(PortedYNode, edges, nodes, nodes))

    return recursive(coordinates_to_ported_leaves(coordinates), expand)


def coordinates_to_ported_points(coordinates: Strategy[Coordinate]
                                 ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, coordinates, coordinates)


def coordinates_to_ported_trapezoids(coordinates: Strategy[Coordinate]
                                     ) -> Strategy[PortedTrapezoid]:
    return (coordinates_to_ported_points_pairs_edges_pairs(coordinates)
            .map(pack(PortedTrapezoid)))


def coordinates_to_ported_x_nodes(coordinates: Strategy[Coordinate]
                                  ) -> Strategy[PortedXNode]:
    return (coordinates_to_ported_points_with_nodes_pairs(coordinates)
            .map(pack(PortedXNode)))


def coordinates_to_ported_y_nodes(coordinates: Strategy[Coordinate]
                                  ) -> Strategy[PortedYNode]:
    return (coordinates_to_ported_edges_with_nodes_pairs(coordinates)
            .map(pack(PortedYNode)))


def coordinates_to_ported_points_pairs_edges_pairs(
        coordinates: Strategy[Coordinate]
) -> Strategy[Tuple[PortedPoint, PortedPoint, PortedEdge, PortedEdge]]:
    edges = coordinates_to_ported_edges(coordinates)
    return (strategies.tuples(
            coordinates_to_sorted_ported_points_pairs(coordinates),
            strategies.tuples(edges, edges))
            .map(pack(add)))


def coordinates_to_sorted_ported_points_pairs(
        coordinates: Strategy[Coordinate]
) -> Strategy[Tuple[PortedPoint, PortedPoint]]:
    return (strategies.lists(coordinates_to_ported_points(coordinates),
                             min_size=2,
                             max_size=2,
                             unique_by=point_to_coordinates)
            .map(tuple)
            .map(sort_points))


def coordinates_to_ported_edges_with_nodes_pairs(
        coordinates: Strategy[Coordinate]) -> Strategy[Tuple[PortedEdge,
                                                             PortedNode,
                                                             PortedNode]]:
    nodes = coordinates_to_ported_nodes(coordinates)
    return strategies.tuples(coordinates_to_ported_edges(coordinates),
                             nodes, nodes)


def coordinates_to_ported_points_with_nodes_pairs(
        coordinates: Strategy[Coordinate]) -> Strategy[Tuple[PortedPoint,
                                                             PortedNode,
                                                             PortedNode]]:
    nodes = coordinates_to_ported_nodes(coordinates)
    return strategies.tuples(coordinates_to_ported_points(coordinates),
                             nodes, nodes)


def to_bound_with_ported_bounding_boxes_pair(empty: bool,
                                             first_x: float,
                                             first_y: float,
                                             second_x: float,
                                             second_y: float
                                             ) -> BoundPortedBoundingBoxesPair:
    left_x, right_x = sorted((first_x, second_x))
    lower_y, upper_y = sorted((first_y, second_y))
    return (BoundBoundingBox(empty, BoundPoint(left_x, lower_y),
                             BoundPoint(right_x, upper_y)),
            PortedBoundingBox(empty, PortedPoint(left_x, lower_y),
                              PortedPoint(right_x, upper_y)))


def to_bound_with_ported_edges_pair(left_points: BoundPortedPointsPair,
                                    right_points: BoundPortedPointsPair
                                    ) -> BoundPortedEdgesPair:
    bound_left, ported_left = left_points
    bound_right, ported_right = right_points
    return (BoundEdge(bound_left, bound_right),
            PortedEdge(ported_left, ported_right))


def to_bound_with_ported_leaves_pair(bound_trapezoid: BoundTrapezoid,
                                     ported_trapezoid: PortedTrapezoid
                                     ) -> BoundPortedLeavesPair:
    return BoundLeaf(bound_trapezoid), PortedLeaf(ported_trapezoid)


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_trapezoids_pair(left_points: BoundPortedPointsPair,
                                         right_points: BoundPortedPointsPair,
                                         below_edges: BoundPortedEdgesPair,
                                         above_edges: BoundPortedEdgesPair
                                         ) -> BoundPortedTrapezoidsPair:
    bound_left, ported_left = left_points
    bound_right, ported_right = right_points
    bound_below, ported_below = below_edges
    bound_above, ported_above = above_edges
    return (BoundTrapezoid(bound_left, bound_right, bound_below,
                           bound_above),
            PortedTrapezoid(ported_left, ported_right, ported_below,
                            ported_above))


def to_bound_with_ported_x_nodes_pair(points: BoundPortedPointsPair,
                                      left_nodes: BoundPortedNodesPair,
                                      right_nodes: BoundPortedNodesPair
                                      ) -> BoundPortedXNodesPair:
    bound_point, ported_point = points
    bound_left, ported_left = left_nodes
    bound_right, ported_right = right_nodes
    return (BoundXNode(bound_point, bound_left, bound_right),
            PortedXNode(ported_point, ported_left, ported_right))


def to_bound_with_ported_y_nodes_pair(edges: BoundPortedEdgesPair,
                                      below_nodes: BoundPortedNodesPair,
                                      above_nodes: BoundPortedNodesPair
                                      ) -> BoundPortedYNodesPair:
    bound_edge, ported_edge = edges
    bound_below, ported_below = below_nodes
    bound_above, ported_above = above_nodes
    return (BoundYNode(bound_edge, bound_below, bound_above),
            PortedYNode(ported_edge, ported_below, ported_above))


recursive = partial(strategies.recursive,
                    max_leaves=5)


def to_pairs(elements: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(elements, elements)


def to_triplets(elements: Strategy[Domain]
                ) -> Strategy[Tuple[Domain, Domain, Domain]]:
    return strategies.tuples(elements, elements, elements)
