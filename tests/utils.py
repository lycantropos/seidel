import pickle
import sys
from typing import (Tuple,
                    TypeVar)

from _seidel import Point as BoundPoint
from hypothesis.strategies import SearchStrategy

from seidel.point import Point as PortedPoint

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]

MAX_FLOAT_DIGITS_COUNT = sys.float_info.dig // 2
MAX_VALUE = 10 ** 6
MIN_VALUE = -MAX_VALUE


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def pickle_round_trip(object_: Domain) -> Domain:
    return pickle.loads(pickle.dumps(object_))


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y
