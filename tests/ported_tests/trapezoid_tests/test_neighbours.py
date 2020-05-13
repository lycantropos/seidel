from typing import Tuple

from _seidel import Trapezoid
from hypothesis import given

from . import strategies


@given(strategies.trapezoids_pairs)
def test_lower_left(trapezoids_pair: Tuple[Trapezoid, Trapezoid]) -> None:
    first_trapezoid, second_trapezoid = trapezoids_pair

    first_trapezoid.lower_left = second_trapezoid

    assert first_trapezoid.lower_left == second_trapezoid


@given(strategies.trapezoids_pairs)
def test_lower_right(trapezoids_pair: Tuple[Trapezoid, Trapezoid]) -> None:
    first_trapezoid, second_trapezoid = trapezoids_pair

    first_trapezoid.lower_right = second_trapezoid

    assert first_trapezoid.lower_right == second_trapezoid


@given(strategies.trapezoids_pairs)
def test_upper_left(trapezoids_pair: Tuple[Trapezoid, Trapezoid]) -> None:
    first_trapezoid, second_trapezoid = trapezoids_pair

    first_trapezoid.upper_left = second_trapezoid

    assert first_trapezoid.upper_left == second_trapezoid


@given(strategies.trapezoids_pairs)
def test_upper_right(trapezoids_pair: Tuple[Trapezoid, Trapezoid]) -> None:
    first_trapezoid, second_trapezoid = trapezoids_pair

    first_trapezoid.upper_right = second_trapezoid

    assert first_trapezoid.upper_right == second_trapezoid
