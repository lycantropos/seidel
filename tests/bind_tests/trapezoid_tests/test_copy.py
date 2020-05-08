import copy

from _seidel import Trapezoid
from hypothesis import given

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
