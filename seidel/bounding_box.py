from .point import Point


class BoundingBox:
    __slots__ = 'empty', 'lower', 'upper'

    def __init__(self, empty: bool, lower: Point, upper: Point) -> None:
        self.empty = empty
        self.lower = lower
        self.upper = upper
