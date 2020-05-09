from typing import Tuple

from hypothesis import given

from seidel.leaf import Leaf
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.leaves)
def test_reflexivity(leaf: Leaf) -> None:
    assert leaf == leaf


@given(strategies.leaves_pairs)
def test_symmetry(leaves_pair: Tuple[Leaf, Leaf]) -> None:
    first_leaf, second_leaf = leaves_pair

    assert equivalence(first_leaf == second_leaf,
                       second_leaf == first_leaf)


@given(strategies.leaves_triplets)
def test_transitivity(leaves_triplet: Tuple[Leaf, Leaf, Leaf]) -> None:
    first_leaf, second_leaf, third_leaf = leaves_triplet

    assert implication(first_leaf == second_leaf
                       and second_leaf == third_leaf,
                       first_leaf == third_leaf)


@given(strategies.leaves_pairs)
def test_connection_with_inequality(leaves_pair: Tuple[Leaf, Leaf]) -> None:
    first_leaf, second_leaf = leaves_pair

    assert equivalence(not first_leaf == second_leaf,
                       first_leaf != second_leaf)
