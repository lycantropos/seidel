from reprit.base import generate_repr

from .node import Node
from .point import Point


class XNode(Node):
    __slots__ = 'point', 'left', 'right'

    def __init__(self, point: Point, left: Node, right: Node) -> None:
        self.point = point
        self.left = left
        self.right = right

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'XNode') -> bool:
        return ((self.point == other.point
                 and self.left == other.left
                 and self.right == other.right)
                if isinstance(other, XNode)
                else NotImplemented)
