from .edge import Edge
from .node import Node


class YNode(Node):
    __slots__ = 'edge', 'above', 'below'

    def __init__(self, edge: Edge, above: Node, below: Node) -> None:
        self.edge = edge
        self.above = above
        self.below = below

    def __eq__(self, other: 'YNode') -> bool:
        return ((self.edge == other.edge
                 and self.above is other.above
                 and self.below is other.below)
                if isinstance(other, YNode)
                else NotImplemented)
