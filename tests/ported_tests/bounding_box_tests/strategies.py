from hypothesis import strategies

from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs)

booleans = strategies.booleans()
points_pairs = (coordinates_strategies.map(coordinates_to_ported_points)
                .flatmap(to_pairs))
