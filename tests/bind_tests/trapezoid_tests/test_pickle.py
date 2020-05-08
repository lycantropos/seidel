from _seidel import Trapezoid
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.trapezoids)
def test_round_trip(trapezoid: Trapezoid) -> None:
    assert pickle_round_trip(trapezoid) == trapezoid
