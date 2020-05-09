import sys

from _seidel import Leaf
from hypothesis import given

from . import strategies


@given(strategies.leaves)
def test_basic(leaf: Leaf) -> None:
    result = repr(leaf)

    assert result.startswith(Leaf.__module__)
    assert Leaf.__qualname__ in result


@given(strategies.leaves)
def test_round_trip(leaf: Leaf) -> None:
    result = repr(leaf)

    assert eval(result, sys.modules) == leaf
