from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_edges,
                              coordinates_to_ported_points,
                              coordinates_to_sorted_ported_points_pairs,
                              to_pairs,
                              to_triplets)

coordinates_pairs = coordinates_strategies.flatmap(to_pairs)
points = coordinates_strategies.flatmap(coordinates_to_ported_points)
sorted_points_pairs = (coordinates_strategies
                       .flatmap(coordinates_to_sorted_ported_points_pairs))
edges = coordinates_strategies.flatmap(coordinates_to_ported_edges)
edges_strategies = coordinates_strategies.map(coordinates_to_ported_edges)
edges_pairs = edges_strategies.flatmap(to_pairs)
edges_triplets = edges_strategies.flatmap(to_triplets)
