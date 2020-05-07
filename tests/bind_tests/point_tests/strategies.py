from _seidel import Point
from hypothesis import strategies

from tests.strategies import floats

points = strategies.builds(Point, floats, floats)
