from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points_pairs_edges_pairs,
                              coordinates_to_ported_trapezoids,
                              to_pairs,
                              to_triplets)

points_pairs_edges_pairs = coordinates_strategies.flatmap(
        coordinates_to_ported_points_pairs_edges_pairs)
trapezoids = coordinates_strategies.flatmap(coordinates_to_ported_trapezoids)
trapezoids_strategies = (coordinates_strategies
                         .map(coordinates_to_ported_trapezoids))
trapezoids_pairs = trapezoids_strategies.flatmap(to_pairs)
trapezoids_triplets = trapezoids_strategies.flatmap(to_triplets)
