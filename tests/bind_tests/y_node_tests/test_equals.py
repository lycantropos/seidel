from _seidel import YNode
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.y_nodes)
def test_reflexivity(y_node: YNode) -> None:
    assert y_node == y_node


@given(strategies.y_nodes, strategies.y_nodes)
def test_symmetry(first_y_node: YNode,
                  second_y_node: YNode) -> None:
    assert equivalence(first_y_node == second_y_node,
                       second_y_node == first_y_node)


@given(strategies.y_nodes, strategies.y_nodes, strategies.y_nodes)
def test_transitivity(first_y_node: YNode,
                      second_y_node: YNode,
                      third_y_node: YNode) -> None:
    assert implication(first_y_node == second_y_node
                       and second_y_node == third_y_node,
                       first_y_node == third_y_node)


@given(strategies.y_nodes, strategies.y_nodes)
def test_connection_with_inequality(first_y_node: YNode,
                                    second_y_node: YNode) -> None:
    assert equivalence(not first_y_node == second_y_node,
                       first_y_node != second_y_node)
