from hypothesis import given

from seidel.edge import Edge
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.edges)
def test_round_trip(edge: Edge) -> None:
    assert pickle_round_trip(edge) == edge
