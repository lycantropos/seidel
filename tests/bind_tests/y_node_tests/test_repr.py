from _seidel import YNode
from hypothesis import given

from . import strategies


@given(strategies.y_nodes)
def test_basic(y_node: YNode) -> None:
    result = repr(y_node)

    assert result.startswith(YNode.__module__)
    assert YNode.__qualname__ in result
