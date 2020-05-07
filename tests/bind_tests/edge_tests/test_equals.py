from _seidel import Edge
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.edges)
def test_reflexivity(edge: Edge) -> None:
    assert edge == edge


@given(strategies.edges, strategies.edges)
def test_symmetry(first_edge: Edge, second_edge: Edge) -> None:
    assert equivalence(first_edge == second_edge, second_edge == first_edge)


@given(strategies.edges, strategies.edges, strategies.edges)
def test_transitivity(first_edge: Edge,
                      second_edge: Edge,
                      third_edge: Edge) -> None:
    assert implication(first_edge == second_edge and second_edge == third_edge,
                       first_edge == third_edge)


@given(strategies.edges, strategies.edges)
def test_connection_with_inequality(first_edge: Edge,
                                    second_edge: Edge) -> None:
    assert equivalence(not first_edge == second_edge,
                       first_edge != second_edge)
