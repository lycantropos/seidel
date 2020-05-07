from seidel.point import Point
from tests.strategies import coordinates_strategies
from tests.utils import (pack,
                         to_pairs)

coordinates_pairs = coordinates_strategies.flatmap(to_pairs)
points = coordinates_pairs.map(pack(Point))
