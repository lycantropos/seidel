from copy import copy

from reprit.base import generate_repr

from .point import Point


class BoundingBox:
    __slots__ = 'empty', 'lower', 'upper'

    def __init__(self, empty: bool, lower: Point, upper: Point) -> None:
        self.empty = empty
        self.lower = lower
        self.upper = upper

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'BoundingBox') -> bool:
        return ((self.empty is other.empty
                 and self.lower == other.lower
                 and self.upper == other.upper)
                if isinstance(other, BoundingBox)
                else NotImplemented)

    def add(self, point: Point) -> None:
        if self.empty:
            self.empty = False
            self.lower = copy(point)
            self.upper = copy(point)
        else:
            if point.x < self.lower.x:
                self.lower.x = point.x
            elif point.x > self.upper.x:
                self.upper.x = point.x
            if point.y < self.lower.y:
                self.lower.y = point.y
            elif point.y > self.upper.y:
                self.upper.y = point.y

    def expand(self, delta: Point) -> None:
        if not self.empty:
            self.lower -= delta
            self.upper += delta
