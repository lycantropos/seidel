from typing import Tuple

from hypothesis import given

from seidel.y_node import YNode
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.y_nodes)
def test_reflexivity(y_node: YNode) -> None:
    assert y_node == y_node


@given(strategies.y_nodes_pairs)
def test_symmetry(y_nodes_pair: Tuple[YNode, YNode]) -> None:
    first_y_node, second_y_node = y_nodes_pair

    assert equivalence(first_y_node == second_y_node,
                       second_y_node == first_y_node)


@given(strategies.y_nodes_triplets)
def test_transitivity(y_nodes_triplet: Tuple[YNode, YNode, YNode]) -> None:
    first_y_node, second_y_node, third_y_node = y_nodes_triplet

    assert implication(first_y_node == second_y_node
                       and second_y_node == third_y_node,
                       first_y_node == third_y_node)


@given(strategies.y_nodes_pairs)
def test_connection_with_inequality(y_nodes_pair: Tuple[YNode, YNode]) -> None:
    first_y_node, second_y_node = y_nodes_pair

    assert equivalence(not first_y_node == second_y_node,
                       first_y_node != second_y_node)
