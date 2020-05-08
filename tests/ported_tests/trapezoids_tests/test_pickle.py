from hypothesis import given

from seidel.trapezoid import Trapezoid
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.trapezoids)
def test_round_trip(trapezoid: Trapezoid) -> None:
    assert pickle_round_trip(trapezoid) == trapezoid
