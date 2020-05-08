import sys

from _seidel import Edge
from hypothesis import given

from . import strategies


@given(strategies.edges)
def test_basic(edge: Edge) -> None:
    result = repr(edge)

    assert result.startswith(Edge.__module__)
    assert Edge.__qualname__ in result


@given(strategies.edges)
def test_round_trip(edge: Edge) -> None:
    result = repr(edge)

    assert eval(result, sys.modules) == edge
