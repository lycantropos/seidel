from .point import Point


class BoundingBox:
    __slots__ = 'empty', 'lower', 'upper'

    def __init__(self, empty: bool, lower: Point, upper: Point) -> None:
        self.empty = empty
        self.lower = lower
        self.upper = upper

    def __eq__(self, other: 'BoundingBox') -> bool:
        return ((self.empty is other.empty
                 and self.lower == other.lower
                 and self.upper == other.upper)
                if isinstance(other, BoundingBox)
                else NotImplemented)
