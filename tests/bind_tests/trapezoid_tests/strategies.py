from operator import (add,
                      ne)

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
sorted_points_pairs = to_pairs(points).filter(pack(ne)).map(sort_points)
edges = sorted_points_pairs.map(pack(Edge))
trapezoids = (strategies.tuples(sorted_points_pairs, to_pairs(edges))
              .map(pack(add))
              .map(pack(Trapezoid)))
