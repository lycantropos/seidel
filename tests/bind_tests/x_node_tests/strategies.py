from operator import (add,
                      ne)

from _seidel import (Edge,
                     Leaf,
                     Node,
                     Point,
                     Trapezoid,
                     XNode)
from hypothesis import strategies

from tests.strategies import (floats,
                              to_pairs)
from tests.utils import (Strategy, pack, sort_points)

floats = floats
points = strategies.builds(Point, floats, floats)
sorted_points_pairs = to_pairs(points).filter(pack(ne)).map(sort_points)
edges = sorted_points_pairs.map(pack(Edge))
trapezoids = (strategies.tuples(sorted_points_pairs, to_pairs(edges))
              .map(pack(add))
              .map(pack(Trapezoid)))
leaves = trapezoids.map(Leaf)


def extend(nodes: Strategy[Node]) -> Strategy[Node]:
    return nodes | to_x_nodes(nodes)


def to_x_nodes(nodes: Strategy[Node]) -> Strategy[XNode]:
    return strategies.builds(XNode, points, nodes, nodes)


nodes = strategies.recursive(leaves, extend)
x_nodes = to_x_nodes(nodes)
