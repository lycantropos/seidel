from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs)

coordinates_pairs = coordinates_strategies.flatmap(to_pairs)
points = coordinates_strategies.flatmap(coordinates_to_ported_points)
