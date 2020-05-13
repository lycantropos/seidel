from _seidel import Trapezoid
from hypothesis import given

from . import strategies


@given(strategies.trapezoids, strategies.trapezoids)
def test_lower_left(first_trapezoid: Trapezoid,
                    second_trapezoid: Trapezoid) -> None:
    first_trapezoid.lower_left = second_trapezoid

    assert first_trapezoid.lower_left == second_trapezoid


@given(strategies.trapezoids, strategies.trapezoids)
def test_lower_right(first_trapezoid: Trapezoid,
                     second_trapezoid: Trapezoid) -> None:
    first_trapezoid.lower_right = second_trapezoid

    assert first_trapezoid.lower_right == second_trapezoid


@given(strategies.trapezoids, strategies.trapezoids)
def test_upper_left(first_trapezoid: Trapezoid,
                    second_trapezoid: Trapezoid) -> None:
    first_trapezoid.upper_left = second_trapezoid

    assert first_trapezoid.upper_left == second_trapezoid


@given(strategies.trapezoids, strategies.trapezoids)
def test_upper_right(first_trapezoid: Trapezoid,
                     second_trapezoid: Trapezoid) -> None:
    first_trapezoid.upper_right = second_trapezoid

    assert first_trapezoid.upper_right == second_trapezoid
