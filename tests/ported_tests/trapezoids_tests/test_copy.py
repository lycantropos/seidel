import copy

from hypothesis import given

from seidel.trapezoid import Trapezoid
from . import strategies


@given(strategies.trapezoids)
def test_shallow(trapezoid: Trapezoid) -> None:
    result = copy.copy(trapezoid)

    assert result is not trapezoid
    assert result == trapezoid


@given(strategies.trapezoids)
def test_deep(trapezoid: Trapezoid) -> None:
    result = copy.deepcopy(trapezoid)

    assert result is not trapezoid
    assert result == trapezoid
