from _seidel import Point as BoundPoint

from seidel.point import Point as PortedPoint
from tests.utils import BoundPortedPointsPair


def to_bound_with_ported_points_pair(x: float, y: float
                                     ) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)
