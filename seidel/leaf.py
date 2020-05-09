from .node import Node
from .trapezoid import Trapezoid


class Leaf(Node):
    __slots__ = 'trapezoid',

    def __init__(self, trapezoid: Trapezoid) -> None:
        self.trapezoid = trapezoid

    def __eq__(self, other: 'Leaf') -> bool:
        return (self.trapezoid == other.trapezoid
                if isinstance(other, Leaf)
                else NotImplemented)
