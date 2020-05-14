from typing import Tuple

from hypothesis import given

from tests.utils import (BoundPortedNodesPair,
                         are_bound_ported_nodes_equal,
                         are_bound_ported_nodes_sequences_equal)
from . import strategies


@given(strategies.nested_nodes_with_children_pairs, strategies.nodes_pairs)
def test_basic(first_nodes_with_children_pair: Tuple[BoundPortedNodesPair,
                                                     BoundPortedNodesPair],
               second_nodes_pair: BoundPortedNodesPair) -> None:
    first_nodes, first_children = first_nodes_with_children_pair
    first_bound, first_ported = first_nodes
    first_bound_child, first_ported_child = first_children
    second_bound, second_ported = second_nodes_pair

    first_bound_child.replace_with(second_bound)
    first_ported_child.replace_with(second_ported)

    assert are_bound_ported_nodes_sequences_equal(first_bound_child.parents,
                                                  first_ported_child.parents)
    assert are_bound_ported_nodes_sequences_equal(second_bound.parents,
                                                  second_ported.parents)
    assert are_bound_ported_nodes_equal(first_bound, first_ported)
