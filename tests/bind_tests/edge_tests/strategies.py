from operator import ne

from _seidel import (Edge,
                     Point)
from hypothesis import strategies

from tests.strategies import (floats,
                              to_pairs)
from tests.utils import (pack,
                         sort_points)

floats = floats
points = strategies.builds(Point, floats, floats)
sorted_points = to_pairs(points).filter(pack(ne)).map(sort_points)
edges = sorted_points.map(pack(Edge))
