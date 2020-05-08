from typing import Tuple

from hypothesis import given

from seidel.edge import Edge
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.edges)
def test_reflexivity(edge: Edge) -> None:
    assert edge == edge


@given(strategies.edges_pairs)
def test_symmetry(edges_pair: Tuple[Edge, Edge]) -> None:
    first_edge, second_edge = edges_pair

    assert equivalence(first_edge == second_edge, second_edge == first_edge)


@given(strategies.edges_triplets)
def test_transitivity(edges_triplet: Tuple[Edge, Edge, Edge]) -> None:
    first_edge, second_edge, third_edge = edges_triplet

    assert implication(first_edge == second_edge and second_edge == third_edge,
                       first_edge == third_edge)


@given(strategies.edges_pairs)
def test_connection_with_inequality(edges_pair: Tuple[Edge, Edge]) -> None:
    first_edge, second_edge = edges_pair

    assert equivalence(not first_edge == second_edge,
                       first_edge != second_edge)
