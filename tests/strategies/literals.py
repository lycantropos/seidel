from decimal import Decimal
from fractions import Fraction
from functools import partial

from hypothesis import strategies

from tests.utils import (MAX_FLOAT_DIGITS_COUNT,
                         MAX_VALUE,
                         MIN_VALUE,
                         Strategy)

booleans = strategies.booleans()


def to_floats(min_value: float, max_value: float) -> Strategy[float]:
    return (strategies.floats(min_value, max_value,
                              allow_nan=False,
                              allow_infinity=False)
            .map(to_digits_count))


def to_digits_count(number: float,
                    *,
                    max_digits_count: int = MAX_FLOAT_DIGITS_COUNT) -> float:
    decimal = Decimal(number).normalize()
    _, significant_digits, exponent = decimal.as_tuple()
    significant_digits_count = len(significant_digits)
    if exponent < 0:
        fixed_digits_count = (1 - exponent
                              if exponent <= -significant_digits_count
                              else significant_digits_count)
    else:
        fixed_digits_count = exponent + significant_digits_count
    if fixed_digits_count <= max_digits_count:
        return number
    whole_digits_count = max(significant_digits_count + exponent, 0)
    if whole_digits_count:
        whole_digits_offset = max(whole_digits_count - max_digits_count, 0)
        decimal /= 10 ** whole_digits_offset
        whole_digits_count -= whole_digits_offset
    else:
        decimal *= 10 ** (-exponent - significant_digits_count)
        whole_digits_count = 1
    decimal = round(decimal, max(max_digits_count - whole_digits_count, 0))
    return float(str(decimal))


coordinates_strategies_factories = {
    float: to_floats,
    Fraction: partial(strategies.fractions,
                      max_denominator=MAX_VALUE),
    int: strategies.integers}
coordinates_strategies = strategies.sampled_from(
        [factory(MIN_VALUE, MAX_VALUE)
         for factory in coordinates_strategies_factories.values()])
floats = to_floats(MIN_VALUE, MAX_VALUE)
