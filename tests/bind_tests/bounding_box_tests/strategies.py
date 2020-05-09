from _seidel import (BoundingBox,
                     Point)
from hypothesis import strategies

from tests.strategies import floats

booleans = strategies.booleans()
points = strategies.builds(Point, floats, floats)
bounding_boxes = strategies.builds(BoundingBox, booleans, points, points)
