import sys

from _seidel import Trapezoid
from hypothesis import given

from . import strategies


@given(strategies.trapezoids)
def test_basic(trapezoid: Trapezoid) -> None:
    result = repr(trapezoid)

    assert result.startswith(Trapezoid.__module__)
    assert Trapezoid.__qualname__ in result


@given(strategies.trapezoids)
def test_round_trip(trapezoid: Trapezoid) -> None:
    result = repr(trapezoid)

    assert eval(result, sys.modules) == trapezoid
