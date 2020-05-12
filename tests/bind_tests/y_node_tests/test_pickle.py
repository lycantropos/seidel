from _seidel import YNode
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.y_nodes)
def test_round_trip(y_node: YNode) -> None:
    assert pickle_round_trip(y_node) == y_node
