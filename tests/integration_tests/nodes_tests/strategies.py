from operator import add
from typing import Tuple

from hypothesis import strategies

from tests.strategies import (floats,
                              recursive,
                              to_bound_with_ported_edges_pair,
                              to_bound_with_ported_leaves_pair,
                              to_bound_with_ported_points_pair,
                              to_bound_with_ported_trapezoids_pair,
                              to_bound_with_ported_x_nodes_pair,
                              to_bound_with_ported_y_nodes_pair,
                              to_pairs)
from tests.utils import (BoundPortedNodesPair,
                         BoundPortedXNodesPair,
                         BoundPortedYNodesPair,
                         Strategy,
                         are_endpoints_non_degenerate,
                         node_to_children,
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


def to_nested_nodes_pairs(nodes_pairs: Strategy[BoundPortedNodesPair]
                          ) -> Strategy[BoundPortedNodesPair]:
    return to_x_nodes_pairs(nodes_pairs) | to_y_nodes_pairs(nodes_pairs)


def to_x_nodes_pairs(nodes_pairs: Strategy[BoundPortedNodesPair]
                     ) -> Strategy[BoundPortedXNodesPair]:
    return strategies.builds(to_bound_with_ported_x_nodes_pair,
                             points_pairs, nodes_pairs, nodes_pairs)


def to_y_nodes_pairs(nodes_pairs: Strategy[BoundPortedNodesPair]
                     ) -> Strategy[BoundPortedYNodesPair]:
    return strategies.builds(to_bound_with_ported_y_nodes_pair,
                             edges_pairs, nodes_pairs, nodes_pairs)


nodes_pairs = recursive(leaves_pairs, to_nested_nodes_pairs)
nested_nodes_pairs = to_nested_nodes_pairs(nodes_pairs)


def to_nested_nodes_with_children_pairs(
        nodes_pair: BoundPortedNodesPair
) -> Strategy[Tuple[BoundPortedNodesPair, BoundPortedNodesPair]]:
    bound, ported = nodes_pair
    nodes_children_pairs = tuple(zip(node_to_children(bound),
                                     node_to_children(ported)))
    return strategies.tuples(strategies.just(nodes_pair),
                             strategies.sampled_from(nodes_children_pairs))


nested_nodes_with_children_pairs = nested_nodes_pairs.flatmap(
        to_nested_nodes_with_children_pairs)
