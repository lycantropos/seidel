import copy

from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         are_bound_ported_points_equal)
from . import strategies


@given(strategies.points_pairs)
def test_shallow(points_pair: BoundPortedPointsPair) -> None:
    bound, ported = points_pair

    assert are_bound_ported_points_equal(copy.copy(bound), copy.copy(ported))


@given(strategies.points_pairs)
def test_deep(points_pair: BoundPortedPointsPair) -> None:
    bound, ported = points_pair

    assert are_bound_ported_points_equal(copy.deepcopy(bound),
                                         copy.deepcopy(ported))
