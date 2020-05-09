from _seidel import XNode
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.x_nodes)
def test_reflexivity(x_node: XNode) -> None:
    assert x_node == x_node


@given(strategies.x_nodes, strategies.x_nodes)
def test_symmetry(first_x_node: XNode,
                  second_x_node: XNode) -> None:
    assert equivalence(first_x_node == second_x_node,
                       second_x_node == first_x_node)


@given(strategies.x_nodes, strategies.x_nodes, strategies.x_nodes)
def test_transitivity(first_x_node: XNode,
                      second_x_node: XNode,
                      third_x_node: XNode) -> None:
    assert implication(first_x_node == second_x_node
                       and second_x_node == third_x_node,
                       first_x_node == third_x_node)


@given(strategies.x_nodes, strategies.x_nodes)
def test_connection_with_inequality(first_x_node: XNode,
                                    second_x_node: XNode) -> None:
    assert equivalence(not first_x_node == second_x_node,
                       first_x_node != second_x_node)
