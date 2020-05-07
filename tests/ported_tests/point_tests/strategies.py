from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs,
                              to_triplets)

coordinates_pairs = coordinates_strategies.flatmap(to_pairs)
points = coordinates_strategies.flatmap(coordinates_to_ported_points)
points_strategies = coordinates_strategies.map(coordinates_to_ported_points)
points_pairs = points_strategies.flatmap(to_pairs)
points_triplets = points_strategies.flatmap(to_triplets)
