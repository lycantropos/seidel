from operator import ne

from _seidel import (Edge,
                     Point,
                     Trapezoid)
from hypothesis import strategies

from tests.strategies import (floats,
                              to_pairs)
from tests.utils import (pack,
                         sort_points)

floats = floats
points = strategies.builds(Point, floats, floats)
edges = to_pairs(points).filter(pack(ne)).map(sort_points).map(pack(Edge))
trapezoids = strategies.builds(Trapezoid, points, points, edges, edges)
