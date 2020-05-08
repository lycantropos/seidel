from reprit.base import generate_repr

from .point import Point


class Edge:
    __slots__ = 'left', 'right'

    def __init__(self, left: Point, right: Point) -> None:
        self.left = left
        self.right = right

    __repr__ = generate_repr(__init__)
