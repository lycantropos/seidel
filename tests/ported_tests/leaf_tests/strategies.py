from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_leaves,
                              coordinates_to_ported_trapezoids,
                              to_pairs,
                              to_triplets)

trapezoids = coordinates_strategies.flatmap(coordinates_to_ported_trapezoids)
leaves = coordinates_strategies.flatmap(coordinates_to_ported_leaves)
leaves_strategies = coordinates_strategies.map(coordinates_to_ported_leaves)
leaves_pairs = leaves_strategies.flatmap(to_pairs)
leaves_triplets = leaves_strategies.flatmap(to_triplets)
