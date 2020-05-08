from typing import Tuple

from hypothesis import strategies

from seidel.edge import Edge
from seidel.hints import Coordinate
from tests.utils import (BoundBoundingBox,
                         BoundEdge,
                         BoundPoint,
                         BoundPortedBoundingBoxesPair,
                         BoundPortedEdgesPair,
                         BoundPortedPointsPair,
                         Domain,
                         PortedBoundingBox,
                         PortedEdge,
                         PortedPoint,
                         Strategy,
                         pack,
                         point_to_coordinates,
                         sort_points)


def coordinates_to_ported_points(coordinates: Strategy[Coordinate]
                                 ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, coordinates, coordinates)


def to_pairs(elements: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(elements, elements)


def to_triplets(elements: Strategy[Domain]
                ) -> Strategy[Tuple[Domain, Domain, Domain]]:
    return strategies.tuples(elements, elements, elements)


def to_bound_with_ported_edges_pair(left_points: BoundPortedPointsPair,
                                    right_points: BoundPortedPointsPair
                                    ) -> BoundPortedEdgesPair:
    left_bound, left_ported = left_points
    right_bound, right_ported = right_points
    return (BoundEdge(left_bound, right_bound),
            PortedEdge(left_ported, right_ported))


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


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


def coordinates_to_ported_edges(coordinates: Strategy[Coordinate]
                                ) -> Strategy[PortedEdge]:
    return (coordinates_to_sorted_ported_points_pairs(coordinates)
            .map(pack(Edge)))


def coordinates_to_sorted_ported_points_pairs(
        coordinates: Strategy[Coordinate]
) -> Strategy[Tuple[PortedPoint, PortedPoint]]:
    return (strategies.lists(coordinates_to_ported_points(coordinates),
                             min_size=2,
                             max_size=2,
                             unique_by=point_to_coordinates)
            .map(tuple)
            .map(sort_points))
