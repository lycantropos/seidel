from hypothesis import strategies

from tests.strategies import (floats,
                              to_bound_with_ported_bounding_boxes_pair)

booleans = strategies.booleans()
floats = floats
bounding_boxes_pairs = strategies.builds(
        to_bound_with_ported_bounding_boxes_pair, booleans, floats, floats,
        floats, floats)
