from .edge import Edge
from .point import Point


class Trapezoid:
    __slots__ = 'left', 'right', 'above', 'below'

    def __init__(self,
                 left: Point,
                 right: Point,
                 above: Edge,
                 below: Edge) -> None:
        self.left = left
        self.right = right
        self.above = above
        self.below = below
