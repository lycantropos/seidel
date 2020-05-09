from _seidel import XNode
from hypothesis import given

from . import strategies


@given(strategies.x_nodes)
def test_basic(x_node: XNode) -> None:
    result = repr(x_node)

    assert result.startswith(XNode.__module__)
    assert XNode.__qualname__ in result
