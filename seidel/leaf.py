from reprit.base import generate_repr

from .edge import Edge
from .node import Node
from .point import Point
from .trapezoid import Trapezoid


class Leaf(Node):
    __slots__ = 'trapezoid',

    def __init__(self, trapezoid: Trapezoid) -> None:
        super().__init__()
        self.trapezoid = trapezoid
        trapezoid.trapezoid_node = self

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Leaf') -> bool:
        return (self.trapezoid == other.trapezoid
                if isinstance(other, Leaf)
                else NotImplemented)

    def replace_child(self, old_child: 'Node', new_child: 'Node') -> None:
        raise TypeError('Leaf has no children.')

    def search_edge(self, edge: Edge) -> Trapezoid:
        return self.trapezoid

    def search_point(self, point: Point) -> 'Node':
        return self
