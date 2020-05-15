from _seidel import (Leaf,
                     Trapezoid)
from hypothesis import given

from . import strategies


@given(strategies.trapezoids)
def test_basic(trapezoid: Trapezoid) -> None:
    result = Leaf(trapezoid)

    assert result.trapezoid == trapezoid
    assert result.trapezoid.trapezoid_node == result
