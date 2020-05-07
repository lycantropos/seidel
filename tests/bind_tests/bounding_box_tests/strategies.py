from _seidel import BoundingBox
from hypothesis import strategies

bounding_boxes = strategies.builds(BoundingBox)
