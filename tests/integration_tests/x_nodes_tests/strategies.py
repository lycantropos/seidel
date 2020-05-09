from operator import add

from hypothesis import strategies

from tests.strategies import (floats,
                              recursive,
                              to_bound_with_ported_edges_pair,
                              to_bound_with_ported_leaves_pair,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_trapezoids_pair,
                              to_bound_with_ported_x_nodes_pair,
                              to_pairs)
from tests.utils import (BoundPortedNodesPair,
                         BoundPortedXNodesPair,
                         Strategy,
                         are_endpoints_non_degenerate,
                         pack,
                         sort_endpoints)

points_pairs = strategies.builds(to_bound_with_ported_points_pair, floats,
                                 floats)
sorted_points_pairs_pairs = (to_pairs(points_pairs)
                             .filter(are_endpoints_non_degenerate)
                             .map(sort_endpoints))
edges_pairs = (sorted_points_pairs_pairs
               .map(pack(to_bound_with_ported_edges_pair)))
trapezoids_pairs = (strategies.tuples(sorted_points_pairs_pairs,
                                      to_pairs(edges_pairs))
                    .map(pack(add))
                    .map(pack(to_bound_with_ported_trapezoids_pair)))
leaves_pairs = trapezoids_pairs.map(pack(to_bound_with_ported_leaves_pair))


def to_x_nodes_pairs(nodes_pairs: Strategy[BoundPortedNodesPair]
                     ) -> Strategy[BoundPortedXNodesPair]:
    return strategies.builds(to_bound_with_ported_x_nodes_pair,
                             points_pairs, nodes_pairs, nodes_pairs)


nodes_pairs = recursive(leaves_pairs, to_x_nodes_pairs)
