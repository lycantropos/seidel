from _seidel import Trapezoid
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.trapezoids)
def test_reflexivity(trapezoid: Trapezoid) -> None:
    assert trapezoid == trapezoid


@given(strategies.trapezoids, strategies.trapezoids)
def test_symmetry(first_trapezoid: Trapezoid,
                  second_trapezoid: Trapezoid) -> None:
    assert equivalence(first_trapezoid == second_trapezoid,
                       second_trapezoid == first_trapezoid)


@given(strategies.trapezoids, strategies.trapezoids, strategies.trapezoids)
def test_transitivity(first_trapezoid: Trapezoid,
                      second_trapezoid: Trapezoid,
                      third_trapezoid: Trapezoid) -> None:
    assert implication(first_trapezoid == second_trapezoid
                       and second_trapezoid == third_trapezoid,
                       first_trapezoid == third_trapezoid)


@given(strategies.trapezoids, strategies.trapezoids)
def test_connection_with_inequality(first_trapezoid: Trapezoid,
                                    second_trapezoid: Trapezoid) -> None:
    assert equivalence(not first_trapezoid == second_trapezoid,
                       first_trapezoid != second_trapezoid)
