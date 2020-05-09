from hypothesis import given

from tests.utils import (BoundPortedXNodesPair,
                         equivalence)
from . import strategies


@given(strategies.x_nodes_pairs, strategies.x_nodes_pairs)
def test_basic(first_x_nodes_pair: BoundPortedXNodesPair,
               second_x_nodes_pair: BoundPortedXNodesPair) -> None:
    first_bound, first_ported = first_x_nodes_pair
    second_bound, second_ported = second_x_nodes_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
