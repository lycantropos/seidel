import pickle
import sys
from functools import partial
from typing import (Callable,
                    Iterable,
                    Tuple,
                    TypeVar)

from hypothesis import strategies
from hypothesis.strategies import SearchStrategy

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy

MAX_FLOAT_DIGITS_COUNT = sys.float_info.dig // 2
MAX_VALUE = 10 ** 6
MIN_VALUE = -MAX_VALUE


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def pickle_round_trip(object_: Domain) -> Domain:
    return pickle.loads(pickle.dumps(object_))


def to_pairs(elements: Strategy[Domain]) -> Strategy[Tuple[Domain, Domain]]:
    return strategies.tuples(elements, elements)


def pack(function: Callable[..., Range]
         ) -> Callable[[Iterable[Domain]], Range]:
    return partial(apply, function)


def apply(function: Callable[..., Range],
          args: Iterable[Domain]) -> Range:
    return function(*args)
