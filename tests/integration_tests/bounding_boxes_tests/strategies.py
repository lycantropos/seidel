from typing import (List,
                    Tuple)

from hypothesis import strategies

from tests.strategies import (floats,
                              to_bound_with_ported_bounding_boxes_pair,
                              to_bound_with_ported_points_pair)
from tests.utils import (BoundPoint,
                         BoundPortedPointsPair,
                         PortedPoint)

booleans = strategies.booleans()
floats = floats
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)


def transpose(points_pairs_list: List[BoundPortedPointsPair]
              ) -> Tuple[List[BoundPoint], List[PortedPoint]]:
    return tuple(map(list, zip(*points_pairs_list)))


points_lists_pairs = (strategies.lists(points_pairs,
                                       min_size=1)
                      .map(transpose))
bounding_boxes_pairs = strategies.builds(
        to_bound_with_ported_bounding_boxes_pair, booleans, floats, floats,
        floats, floats)
