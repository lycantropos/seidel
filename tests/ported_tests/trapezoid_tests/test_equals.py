from typing import Tuple

from hypothesis import given

from seidel.trapezoid import Trapezoid
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.trapezoids)
def test_reflexivity(trapezoid: Trapezoid) -> None:
    assert trapezoid == trapezoid


@given(strategies.trapezoids_pairs)
def test_symmetry(trapezoids_pair: Tuple[Trapezoid, Trapezoid]) -> None:
    first_trapezoid, second_trapezoid = trapezoids_pair

    assert equivalence(first_trapezoid == second_trapezoid,
                       second_trapezoid == first_trapezoid)


@given(strategies.trapezoids_triplets)
def test_transitivity(trapezoids_triplet: Tuple[Trapezoid, Trapezoid,
                                                Trapezoid]) -> None:
    first_trapezoid, second_trapezoid, third_trapezoid = trapezoids_triplet

    assert implication(first_trapezoid == second_trapezoid
                       and second_trapezoid == third_trapezoid,
                       first_trapezoid == third_trapezoid)


@given(strategies.trapezoids_pairs)
def test_connection_with_inequality(trapezoids_pair: Tuple[Trapezoid,
                                                           Trapezoid]) -> None:
    first_trapezoid, second_trapezoid = trapezoids_pair

    assert equivalence(not first_trapezoid == second_trapezoid,
                       first_trapezoid != second_trapezoid)
