import copy

from _seidel import YNode
from hypothesis import given

from . import strategies


@given(strategies.y_nodes)
def test_shallow(y_node: YNode) -> None:
    result = copy.copy(y_node)

    assert result is not y_node
    assert result == y_node


@given(strategies.y_nodes)
def test_deep(y_node: YNode) -> None:
    result = copy.deepcopy(y_node)

    assert result is not y_node
    assert result == y_node
