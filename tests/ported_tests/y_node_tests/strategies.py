from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_edges_with_nodes_pairs,
                              coordinates_to_ported_y_nodes,
                              to_pairs,
                              to_triplets)

edges_with_nodes_pairs = coordinates_strategies.flatmap(
        coordinates_to_ported_edges_with_nodes_pairs)
y_nodes = coordinates_strategies.flatmap(coordinates_to_ported_y_nodes)
y_nodes_strategies = coordinates_strategies.map(coordinates_to_ported_y_nodes)
y_nodes_pairs = y_nodes_strategies.flatmap(to_pairs)
y_nodes_triplets = y_nodes_strategies.flatmap(to_triplets)
