from hypothesis import strategies

from seidel.bounding_box import BoundingBox
from seidel.hints import Coordinate
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs)
from tests.utils import Strategy

booleans = strategies.booleans()
points_pairs = (coordinates_strategies.map(coordinates_to_ported_points)
                .flatmap(to_pairs))


def coordinates_to_bounding_boxes(coordinates: Strategy[Coordinate]
                                  ) -> Strategy[BoundingBox]:
    points = coordinates_to_ported_points(coordinates)
    return strategies.builds(BoundingBox, booleans, points, points)


bounding_boxes = coordinates_strategies.flatmap(coordinates_to_bounding_boxes)
