import copy

from hypothesis import given

from seidel.edge import Edge
from . import strategies


@given(strategies.edges)
def test_shallow(edge: Edge) -> None:
    result = copy.copy(edge)

    assert result is not edge
    assert result == edge


@given(strategies.edges)
def test_deep(edge: Edge) -> None:
    result = copy.deepcopy(edge)

    assert result is not edge
    assert result == edge
