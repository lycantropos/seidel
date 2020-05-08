from _seidel import Edge
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.edges)
def test_round_trip(edge: Edge) -> None:
    assert pickle_round_trip(edge) == edge
