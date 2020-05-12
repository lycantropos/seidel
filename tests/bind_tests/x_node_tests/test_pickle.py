from _seidel import XNode
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.x_nodes)
def test_round_trip(x_node: XNode) -> None:
    assert pickle_round_trip(x_node) == x_node
