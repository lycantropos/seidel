from typing import Tuple

from hypothesis import strategies

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
                         Strategy)


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
