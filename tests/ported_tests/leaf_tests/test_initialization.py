from hypothesis import given

from seidel.leaf import Leaf
from seidel.trapezoid import Trapezoid
from . import strategies


@given(strategies.trapezoids)
def test_basic(trapezoid: Trapezoid) -> None:
    result = Leaf(trapezoid)

    assert result.trapezoid == trapezoid
    assert result.trapezoid.trapezoid_node == result
