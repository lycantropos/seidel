from hypothesis import strategies

from tests.strategies import (floats,
                              to_bound_with_ported_bounding_boxes_pair,
                              to_bound_with_ported_points_pair)

booleans = strategies.booleans()
floats = floats
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
bounding_boxes_pairs = strategies.builds(
        to_bound_with_ported_bounding_boxes_pair, booleans, floats, floats,
        floats, floats)
