from .node import Node
from .point import Point


class XNode(Node):
    __slots__ = 'point', 'left', 'right'

    def __init__(self, point: Point, left: Node, right: Node) -> None:
        self.point = point
        self.left = left
        self.right = right
