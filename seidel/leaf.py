from reprit.base import generate_repr

from .node import Node
from .trapezoid import Trapezoid


class Leaf(Node):
    __slots__ = 'trapezoid',

    def __init__(self, trapezoid: Trapezoid) -> None:
        self.trapezoid = trapezoid

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Leaf') -> bool:
        return (self.trapezoid == other.trapezoid
                if isinstance(other, Leaf)
                else NotImplemented)
