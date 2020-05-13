from reprit.base import generate_repr

from .point import Point


class Edge:
    __slots__ = 'left', 'right'

    def __init__(self, left: Point, right: Point) -> None:
        assert right.is_right_of(left), 'Incorrect endpoints order'
        self.left = left
        self.right = right

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Edge') -> bool:
        return (self.left == other.left and self.right == other.right
                if isinstance(other, Edge)
                else NotImplemented)

    def get_point_orientation(self, point: Point) -> int:
        cross_z = (point - self.left).cross_z(self.right - self.left)
        return (1
                if cross_z > 0
                else (-1
                      if cross_z < 0
                      else 0))
