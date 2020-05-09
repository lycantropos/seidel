from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points_pairs_edges_pairs,
                              coordinates_to_ported_trapezoids)

points_pairs_edges_pairs = coordinates_strategies.flatmap(
        coordinates_to_ported_points_pairs_edges_pairs)
trapezoids = coordinates_strategies.flatmap(coordinates_to_ported_trapezoids)
