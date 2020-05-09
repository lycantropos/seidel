from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points_with_nodes_pairs,
                              coordinates_to_ported_x_nodes,
                              to_pairs,
                              to_triplets)

points_with_nodes_pairs = coordinates_strategies.flatmap(
        coordinates_to_ported_points_with_nodes_pairs)
x_nodes = coordinates_strategies.flatmap(coordinates_to_ported_x_nodes)
x_nodes_strategies = coordinates_strategies.map(coordinates_to_ported_x_nodes)
x_nodes_pairs = x_nodes_strategies.flatmap(to_pairs)
x_nodes_triplets = x_nodes_strategies.flatmap(to_triplets)
