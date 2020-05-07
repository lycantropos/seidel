from typing import Tuple

from _seidel import Point as BoundPoint
from hypothesis import strategies

from seidel.hints import Coordinate
from seidel.point import Point as PortedPoint
from tests.utils import (BoundPortedPointsPair,
                         Domain,
                         Strategy)


def coordinates_to_ported_points(coordinates: Strategy[Coordinate]
                                 ) -> Strategy[PortedPoint]:
    return strategies.builds(PortedPoint, coordinates, coordinates)


def to_pairs(elements: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(elements, elements)


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)
