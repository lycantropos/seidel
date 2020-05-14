from abc import (ABC,
                 abstractmethod)
from typing import (Optional,
                    Sequence)

from .edge import Edge
from .trapezoid import Trapezoid


class Node(ABC):
    __slots__ = '_parents',

    def __init__(self) -> None:
        self._parents = []

    @property
    def parents(self) -> Sequence['Node']:
        return self._parents

    @abstractmethod
    def search_edge(self, edge: Edge) -> Optional[Trapezoid]:
        """
        Recursive search for the trapezoid
        which contains the left endpoint of the given edge.
        """

    def has_parent(self, parent: 'Node') -> bool:
        return parent in self._parents

    @abstractmethod
    def replace_child(self, old_child: 'Node', new_child: 'Node') -> None:
        """
        Replaces child node with given one.
        """

    def replace_with(self, other: 'Node') -> None:
        """
        Replaces the node with given one in all parents.
        """
        while self._parents:
            self._parents[0].replace_child(self, other)

    def _add_parent(self, parent: 'Node') -> None:
        assert parent is not None, 'Null parent'
        assert parent is not self, 'Cannot be parent of self'
        assert not self.has_parent(parent), 'Parent already in collection'
        self._parents.append(parent)

    def _remove_parent(self, parent: 'Node') -> None:
        self._parents.remove(parent)
