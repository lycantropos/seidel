from operator import (add,
                      ne)

from _seidel import (Edge,
                     Leaf,
                     Node,
                     Point,
                     Trapezoid,
                     XNode,
                     YNode)
from hypothesis import strategies

from tests.strategies import (floats,
                              recursive,
                              to_pairs)
from tests.utils import (Strategy,
                         pack,
                         sort_points)

points = strategies.builds(Point, floats, floats)
sorted_points_pairs = to_pairs(points).filter(pack(ne)).map(sort_points)
edges = sorted_points_pairs.map(pack(Edge))
trapezoids = (strategies.tuples(sorted_points_pairs, to_pairs(edges))
              .map(pack(add))
              .map(pack(Trapezoid)))
leaves = trapezoids.map(Leaf)


def to_nodes(nodes: Strategy[Node]) -> Strategy[Node]:
    return to_x_nodes(nodes) | to_y_nodes(nodes)


def to_x_nodes(nodes: Strategy[Node]) -> Strategy[YNode]:
    return strategies.builds(XNode, points, nodes, nodes)


def to_y_nodes(nodes: Strategy[Node]) -> Strategy[YNode]:
    return strategies.builds(YNode, edges, nodes, nodes)


nodes = recursive(leaves, to_nodes)
y_nodes = to_y_nodes(nodes)
