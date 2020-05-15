from reprit.base import generate_repr

from .edge import Edge
from .node import Node
from .point import Point
from .trapezoid import Trapezoid


class XNode(Node):
    __slots__ = 'point', 'left', 'right'

    def __init__(self, point: Point, left: Node, right: Node) -> None:
        super().__init__()
        self.point = point
        self.left = left
        self.right = right
        self.left._add_parent(self)
        self.right._add_parent(self)

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'XNode') -> bool:
        return ((self.point == other.point
                 and self.left == other.left
                 and self.right == other.right)
                if isinstance(other, XNode)
                else NotImplemented)

    def replace_child(self, old_child: Node, new_child: Node) -> None:
        assert (self.left is old_child
                or self.right is old_child), 'Not a child Node'
        assert new_child is not None, 'Null child node'
        if self.left is old_child:
            self.left = new_child
        else:
            self.right = new_child
        old_child._remove_parent(self)
        new_child._add_parent(self)

    def search_edge(self, edge: Edge) -> Trapezoid:
        if edge.left is self.point:
            return self.right.search_edge(edge)
        elif edge.left.is_right_of(self.point):
            return self.right.search_edge(edge)
        else:
            return self.left.search_edge(edge)

    def search_point(self, point: Point) -> 'Node':
        if point == self.point:
            return self
        elif point.is_right_of(self.point):
            return self.right.search_point(point)
        else:
            return self.left.search_point(point)
