from typing import Optional

from reprit.base import generate_repr

from .edge import Edge
from .node import Node
from .trapezoid import Trapezoid


class YNode(Node):
    __slots__ = 'edge', 'above', 'below'

    def __init__(self, edge: Edge, below: Node, above: Node) -> None:
        super().__init__()
        self.edge = edge
        self.below = below
        self.above = above

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'YNode') -> bool:
        return ((self.edge == other.edge
                 and self.above == other.above
                 and self.below == other.below)
                if isinstance(other, YNode)
                else NotImplemented)

    def replace_child(self, old_child: 'Node', new_child: 'Node') -> None:
        assert (self.below is old_child
                or self.above is old_child), 'Not a child node'
        assert new_child is not None, 'Null child node'
        if self.below is old_child:
            self.below = new_child
        else:
            self.above = new_child
        old_child.remove_parent(self)
        new_child.add_parent(self)

    def search_edge(self, edge: Edge) -> Optional[Trapezoid]:
        if edge.left == self.edge.left:
            # Coinciding left edge points.
            if edge.get_slope() == self.edge.get_slope():
                return None
            if edge.get_slope() > self.edge.get_slope():
                return self.above.search_edge(edge)
            else:
                return self.below.search_edge(edge)
        elif edge.right == self.edge.right:
            # Coinciding right edge points.
            if edge.get_slope() == self.edge.get_slope():
                return None
            elif edge.get_slope() > self.edge.get_slope():
                return self.below.search_edge(edge)
            else:
                return self.above.search_edge(edge)
        else:
            orientation = self.edge.get_point_orientation(edge.left)
            if orientation < 0:
                return self.above.search_edge(edge)
            elif orientation > 0:
                return self.below.search_edge(edge)
            else:
                return None
