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

    def __eq__(self, other: 'Trapezoid') -> bool:
        return ((self.left == other.left and self.right == other.right
                 and self.above == other.above and self.below == other.below)
                if isinstance(other, Trapezoid)
                else NotImplemented)
