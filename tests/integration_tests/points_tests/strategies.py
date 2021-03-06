from hypothesis import strategies

from tests.strategies import (floats,
                              to_bound_with_ported_points_pair)
from tests.utils import (MAX_VALUE,
                         MIN_VALUE)

floats = floats
scales = strategies.integers(MIN_VALUE, MAX_VALUE)
points_pairs = strategies.builds(to_bound_with_ported_points_pair,
                                 floats, floats)
