import pickle
import sys
from functools import partial
from typing import (Callable,
                    Iterable,
                    Tuple,
                    TypeVar,
                    Union)

from _seidel import (BoundingBox as BoundBoundingBox,
                     Edge as BoundEdge,
                     Point as BoundPoint)
from hypothesis.strategies import SearchStrategy

from seidel.bounding_box import BoundingBox as PortedBoundingBox
from seidel.edge import Edge as PortedEdge
from seidel.hints import Coordinate
from seidel.point import Point as PortedPoint

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy
BoundBoundingBox = BoundBoundingBox
BoundPoint = BoundPoint
BoundEdge = BoundEdge
PortedBoundingBox = PortedBoundingBox
PortedEdge = PortedEdge
PortedPoint = PortedPoint
BoundPortedBoundingBoxesPair = Tuple[BoundBoundingBox, PortedBoundingBox]
BoundPortedEdgesPair = Tuple[BoundEdge, PortedEdge]
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


def pack(function: Callable[..., Range]
         ) -> Callable[[Iterable[Domain]], Range]:
    return partial(apply, function)


def apply(function: Callable[..., Range],
          args: Iterable[Domain]) -> Range:
    return function(*args)


def are_bound_ported_bounding_boxes_equal(bound: BoundBoundingBox,
                                          ported: PortedBoundingBox) -> bool:
    return (bound.empty is ported.empty
            and are_bound_ported_points_equal(bound.lower, ported.lower)
            and are_bound_ported_points_equal(bound.upper, ported.upper))


def are_bound_ported_edges_equal(bound: BoundEdge, ported: PortedEdge) -> bool:
    return (are_bound_ported_points_equal(bound.left, ported.left)
            and are_bound_ported_points_equal(bound.right, ported.right))


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def point_to_coordinates(point: Union[BoundPoint, PortedPoint]
                         ) -> Tuple[Coordinate, Coordinate]:
    return point.x, point.y
