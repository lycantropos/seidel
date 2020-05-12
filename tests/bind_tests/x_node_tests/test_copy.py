import copy

from _seidel import XNode
from hypothesis import given

from . import strategies


@given(strategies.x_nodes)
def test_shallow(x_node: XNode) -> None:
    result = copy.copy(x_node)

    assert result is not x_node
    assert result == x_node


@given(strategies.x_nodes)
def test_deep(x_node: XNode) -> None:
    result = copy.deepcopy(x_node)

    assert result is not x_node
    assert result == x_node
