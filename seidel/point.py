from .hints import Coordinate


class Point:
    __slots__ = 'x', 'y'

    def __init__(self, x: Coordinate, y: Coordinate) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: 'Point') -> bool:
        return (self.x == other.x and self.y == other.y
                if isinstance(other, Point)
                else NotImplemented)
