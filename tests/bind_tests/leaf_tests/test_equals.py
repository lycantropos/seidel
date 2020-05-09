from _seidel import Leaf
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.leaves)
def test_reflexivity(leaf: Leaf) -> None:
    assert leaf == leaf


@given(strategies.leaves, strategies.leaves)
def test_symmetry(first_leaf: Leaf,
                  second_leaf: Leaf) -> None:
    assert equivalence(first_leaf == second_leaf,
                       second_leaf == first_leaf)


@given(strategies.leaves, strategies.leaves, strategies.leaves)
def test_transitivity(first_leaf: Leaf,
                      second_leaf: Leaf,
                      third_leaf: Leaf) -> None:
    assert implication(first_leaf == second_leaf
                       and second_leaf == third_leaf,
                       first_leaf == third_leaf)


@given(strategies.leaves, strategies.leaves)
def test_connection_with_inequality(first_leaf: Leaf,
                                    second_leaf: Leaf) -> None:
    assert equivalence(not first_leaf == second_leaf,
                       first_leaf != second_leaf)
