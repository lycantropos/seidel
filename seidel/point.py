from .hints import Coordinate


class Point:
    __slots__ = 'x', 'y'

    def __init__(self, x: Coordinate, y: Coordinate) -> None:
        self.x = x
        self.y = y
