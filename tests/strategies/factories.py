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
                         BoundPortedPointsPair,
                         BoundPortedTrapezoidsPair,
                         BoundTrapezoid,
                         Domain,
                         PortedBoundingBox,
                         PortedEdge,
                         PortedLeaf,
                         PortedPoint,
                         PortedTrapezoid,
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


def coordinates_to_ported_points(coordinates: Strategy[Coordinate]
                                 ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, coordinates, coordinates)


def coordinates_to_ported_trapezoids(coordinates: Strategy[Coordinate]
                                     ) -> Strategy[PortedTrapezoid]:
    return (coordinates_to_ported_points_pairs_edges_pairs(coordinates)
            .map(pack(PortedTrapezoid)))


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


def to_bound_with_ported_bounding_boxes_pair(empty: bool,
                                             lower_x: float,
                                             lower_y: float,
                                             upper_x: float,
                                             upper_y: float
                                             ) -> BoundPortedBoundingBoxesPair:
    return (PortedBoundingBox(empty, PortedPoint(lower_x, lower_y),
                              PortedPoint(upper_x, upper_y)),
            BoundBoundingBox(empty, BoundPoint(lower_x, lower_y),
                             BoundPoint(upper_x, upper_y)))


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
                                         above_edges: BoundPortedEdgesPair,
                                         below_edges: BoundPortedEdgesPair
                                         ) -> BoundPortedTrapezoidsPair:
    bound_left, ported_left = left_points
    bound_right, ported_right = right_points
    bound_above, ported_above = above_edges
    bound_below, ported_below = below_edges
    return (BoundTrapezoid(bound_left, bound_right, bound_above,
                           bound_below),
            PortedTrapezoid(ported_left, ported_right, ported_above,
                            ported_below))


recursive = partial(strategies.recursive,
                    max_leaves=10)


def to_pairs(elements: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(elements, elements)


def to_triplets(elements: Strategy[Domain]
                ) -> Strategy[Tuple[Domain, Domain, Domain]]:
    return strategies.tuples(elements, elements, elements)
