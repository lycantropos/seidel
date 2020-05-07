from typing import Tuple

from _seidel import (BoundingBox as BoundBoundingBox,
                     Point as BoundPoint)
from hypothesis import strategies

from seidel.bounding_box import BoundingBox as PortedBoundingBox
from seidel.hints import Coordinate
from seidel.point import Point as PortedPoint
from tests.utils import (BoundPortedBoundingBoxesPair,
                         BoundPortedPointsPair,
                         Domain, Strategy)


def coordinates_to_ported_points(coordinates: Strategy[Coordinate]
                                 ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, coordinates, coordinates)


def to_pairs(elements: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(elements, elements)


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
