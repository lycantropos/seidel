from typing import Tuple

from hypothesis import given

from seidel.x_node import XNode
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.x_nodes)
def test_reflexivity(x_node: XNode) -> None:
    assert x_node == x_node


@given(strategies.x_nodes_pairs)
def test_symmetry(x_nodes_pair: Tuple[XNode, XNode]) -> None:
    first_x_node, second_x_node = x_nodes_pair

    assert equivalence(first_x_node == second_x_node,
                       second_x_node == first_x_node)


@given(strategies.x_nodes_triplets)
def test_transitivity(x_nodes_triplet: Tuple[XNode, XNode, XNode]) -> None:
    first_x_node, second_x_node, third_x_node = x_nodes_triplet

    assert implication(first_x_node == second_x_node
                       and second_x_node == third_x_node,
                       first_x_node == third_x_node)


@given(strategies.x_nodes_pairs)
def test_connection_with_inequality(x_nodes_pair: Tuple[XNode, XNode]) -> None:
    first_x_node, second_x_node = x_nodes_pair

    assert equivalence(not first_x_node == second_x_node,
                       first_x_node != second_x_node)
