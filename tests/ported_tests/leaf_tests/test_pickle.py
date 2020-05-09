from hypothesis import given

from seidel.leaf import Leaf
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.leaves)
def test_round_trip(leaf: Leaf) -> None:
    assert pickle_round_trip(leaf) == leaf
