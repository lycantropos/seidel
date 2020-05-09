from .edge import Edge
from .node import Node


class YNode(Node):
    __slots__ = 'edge', 'above', 'below'

    def __init__(self, edge: Edge, above: Node, below: Node) -> None:
        self.edge = edge
        self.above = above
        self.below = below
