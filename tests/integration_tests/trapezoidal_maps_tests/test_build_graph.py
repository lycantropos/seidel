from _seidel import build_graph as bound_build_graph
from hypothesis import given

from seidel.trapezoidal_map import build_graph as ported_build_graph
from tests.utils import (BoundPortedPointsListsPair,
                         are_bound_ported_nodes_equal)
from . import strategies


@given(strategies.contours_pairs)
def test_basic(contours_pair: BoundPortedPointsListsPair) -> None:
    bound_contour, ported_contour = contours_pair

    bound, ported = (bound_build_graph(bound_contour, False),
                     ported_build_graph(ported_contour, False))

    assert are_bound_ported_nodes_equal(bound, ported)
