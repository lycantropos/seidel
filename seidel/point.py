from reprit.base import generate_repr

from .hints import Coordinate


class Point:
    __slots__ = 'x', 'y'

    def __init__(self, x: Coordinate, y: Coordinate) -> None:
        self.x = x
        self.y = y

    __repr__ = generate_repr(__init__)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other: 'Point') -> bool:
        return (self.x == other.x and self.y == other.y
                if isinstance(other, Point)
                else NotImplemented)

    def __mul__(self, scale: Coordinate) -> 'Point':
        return Point(self.x * scale, self.y * scale)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def cross_z(self, other: 'Point') -> Coordinate:
        return self.x * other.y - self.y * other.x

    def is_right_of(self, other: 'Point') -> bool:
        return (self.x, self.y) > (other.x, other.y)
