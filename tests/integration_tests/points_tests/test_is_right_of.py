from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         equivalence)
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs)
def test_basic(first_points_pair: BoundPortedPointsPair,
               second_points_pair: BoundPortedPointsPair) -> None:
    first_bound, first_ported = first_points_pair
    second_bound, second_ported = second_points_pair

    assert equivalence(first_bound.is_right_of(second_bound),
                       first_ported.is_right_of(second_ported))
