from hypothesis_geometry import planar
from hypothesis_geometry.hints import Contour

from tests.strategies import floats
from tests.utils import (BoundPoint,
                         BoundPortedPointsListsPair,
                         PortedPoint)


def to_bound_with_ported_contours(raw: Contour) -> BoundPortedPointsListsPair:
    return ([BoundPoint(x, y) for x, y in raw],
            [PortedPoint(x, y) for x, y in raw])


contours_pairs = planar.contours(floats).map(to_bound_with_ported_contours)
