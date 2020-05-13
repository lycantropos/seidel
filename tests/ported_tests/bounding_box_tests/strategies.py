from typing import Tuple

from hypothesis import strategies

from seidel.bounding_box import BoundingBox
from seidel.hints import Coordinate
from seidel.point import Point
from tests.strategies import (coordinates_strategies,
                              coordinates_to_ported_points,
                              to_pairs)
from tests.utils import Strategy

booleans = strategies.booleans()
points_pairs = (coordinates_strategies.map(coordinates_to_ported_points)
                .flatmap(to_pairs))


def coordinates_to_bounding_boxes(coordinates: Strategy[Coordinate]
                                  ) -> Strategy[BoundingBox]:
    def to_bounding_box(empty: bool,
                        first_x: Coordinate, first_y: Coordinate,
                        second_x: Coordinate, second_y: Coordinate
                        ) -> BoundingBox:
        left_x, right_x = sorted((first_x, second_x))
        lower_y, upper_y = sorted((first_y, second_y))
        return BoundingBox(empty, Point(left_x, lower_y),
                           Point(right_x, upper_y))

    return strategies.builds(to_bounding_box,
                             booleans, coordinates, coordinates,
                             coordinates, coordinates)


bounding_boxes = coordinates_strategies.flatmap(coordinates_to_bounding_boxes)


def coordinates_to_bounding_boxes_with_points(coordinates: Strategy[Coordinate]
                                              ) -> Strategy[Tuple[BoundingBox,
                                                                  Point]]:
    return strategies.tuples(coordinates_to_bounding_boxes(coordinates),
                             coordinates_to_ported_points(coordinates))


bounding_boxes_with_points = coordinates_strategies.flatmap(
        coordinates_to_bounding_boxes_with_points)
