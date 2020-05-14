import math

from _seidel import Edge
from hypothesis import given

from tests.utils import (equivalence,
                         is_edge_horizontal,
                         is_edge_vertical)
from . import strategies


@given(strategies.edges)
def test_basic(edge: Edge) -> None:
    assert isinstance(edge.slope, float)


@given(strategies.edges)
def test_properties(edge: Edge) -> None:
    result = edge.slope

    assert equivalence(result == 0,
                       is_edge_horizontal(edge))
    assert equivalence(math.isinf(result),
                       is_edge_vertical(edge))
