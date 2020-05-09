import copy

from hypothesis import given

from seidel.leaf import Leaf
from . import strategies


@given(strategies.leaves)
def test_shallow(leaf: Leaf) -> None:
    result = copy.copy(leaf)

    assert result is not leaf
    assert result == leaf


@given(strategies.leaves)
def test_deep(leaf: Leaf) -> None:
    result = copy.deepcopy(leaf)

    assert result is not leaf
    assert result == leaf
