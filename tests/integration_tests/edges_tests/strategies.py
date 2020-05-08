from typing import Tuple

from hypothesis import strategies

from tests.strategies import (floats,
                              to_bound_with_ported_edges_pair,
                              to_bound_with_ported_points_pair,
                              to_pairs)
from tests.utils import (BoundEdge,
                         PortedEdge,
                         pack)

points_pairs = strategies.builds(to_bound_with_ported_points_pair, floats,
                                 floats)


def are_endpoints_non_degenerate(endpoints: Tuple[Tuple[BoundEdge,
                                                        PortedEdge],
                                                  Tuple[BoundEdge,
                                                        PortedEdge]]) -> bool:
    (first_bound, _), (second_bound, _) = endpoints
    return first_bound != second_bound


def sort_endpoints(endpoints: Tuple[Tuple[BoundEdge, PortedEdge],
                                    Tuple[BoundEdge, PortedEdge]]
                   ) -> Tuple[Tuple[BoundEdge, PortedEdge],
                              Tuple[BoundEdge, PortedEdge]]:
    (first_bound, _), (second_bound, _) = endpoints
    return (endpoints
            if second_bound.is_right_of(first_bound)
            else endpoints[::-1])


sorted_points_pairs_pairs = (to_pairs(points_pairs)
                             .filter(are_endpoints_non_degenerate)
                             .map(sort_endpoints))
edges_pairs = (sorted_points_pairs_pairs
               .map(pack(to_bound_with_ported_edges_pair)))
