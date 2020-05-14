import pickle
import sys
from functools import partial
from typing import (Callable,
                    Iterable,
                    Tuple,
                    TypeVar)

from _seidel import (BoundingBox as BoundBoundingBox,
                     Edge as BoundEdge,
                     Leaf as BoundLeaf,
                     Node as BoundNode,
                     Point as BoundPoint,
                     Trapezoid as BoundTrapezoid,
                     XNode as BoundXNode,
                     YNode as BoundYNode)
from hypothesis.strategies import SearchStrategy

from seidel.bounding_box import BoundingBox as PortedBoundingBox
from seidel.edge import Edge as PortedEdge
from seidel.hints import Coordinate
from seidel.leaf import Leaf as PortedLeaf
from seidel.node import Node as PortedNode
from seidel.point import Point as PortedPoint
from seidel.trapezoid import Trapezoid as PortedTrapezoid
from seidel.x_node import XNode as PortedXNode
from seidel.y_node import YNode as PortedYNode

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy
BoundBoundingBox = BoundBoundingBox
BoundEdge = BoundEdge
BoundLeaf = BoundLeaf
BoundNode = BoundNode
BoundPoint = BoundPoint
BoundTrapezoid = BoundTrapezoid
BoundXNode = BoundXNode
BoundYNode = BoundYNode
PortedBoundingBox = PortedBoundingBox
PortedEdge = PortedEdge
PortedLeaf = PortedLeaf
PortedNode = PortedNode
PortedPoint = PortedPoint
PortedTrapezoid = PortedTrapezoid
PortedXNode = PortedXNode
PortedYNode = PortedYNode
AnyEdge = TypeVar('AnyEdge', BoundEdge, PortedEdge)
AnyPoint = TypeVar('AnyPoint', BoundPoint, PortedPoint)
BoundPortedBoundingBoxesPair = Tuple[BoundBoundingBox, PortedBoundingBox]
BoundPortedEdgesPair = Tuple[BoundEdge, PortedEdge]
BoundPortedLeavesPair = Tuple[BoundLeaf, PortedLeaf]
BoundPortedNodesPair = Tuple[BoundNode, PortedNode]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedTrapezoidsPair = Tuple[BoundTrapezoid, PortedTrapezoid]
BoundPortedXNodesPair = Tuple[BoundXNode, PortedXNode]
BoundPortedYNodesPair = Tuple[BoundYNode, PortedYNode]

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


def are_bound_ported_leaves_equal(bound: BoundLeaf,
                                  ported: PortedLeaf) -> bool:
    return are_bound_ported_trapezoids_equal(bound.trapezoid, ported.trapezoid)


def are_bound_ported_nodes_equal(bound: BoundNode,
                                 ported: PortedNode) -> bool:
    if isinstance(bound, BoundLeaf):
        assert isinstance(ported, PortedLeaf)
        return are_bound_ported_leaves_equal(bound, ported)
    elif isinstance(bound, BoundXNode):
        assert isinstance(ported, PortedXNode)
        return are_bound_ported_x_nodes_equal(bound, ported)
    else:
        assert isinstance(ported, PortedYNode)
        return are_bound_ported_y_nodes_equal(bound, ported)


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_trapezoids_equal(bound: BoundTrapezoid,
                                      ported: PortedTrapezoid) -> bool:
    return (are_bound_ported_points_equal(bound.left, ported.left)
            and are_bound_ported_points_equal(bound.right, ported.right)
            and are_bound_ported_edges_equal(bound.above, ported.above)
            and are_bound_ported_edges_equal(bound.below, ported.below))


def are_bound_ported_x_nodes_equal(bound: BoundXNode,
                                   ported: PortedXNode) -> bool:
    return (are_bound_ported_points_equal(bound.point, ported.point)
            and are_bound_ported_nodes_equal(bound.left, ported.left)
            and are_bound_ported_nodes_equal(bound.right, ported.right))


def are_bound_ported_y_nodes_equal(bound: BoundYNode,
                                   ported: PortedYNode) -> bool:
    return (are_bound_ported_edges_equal(bound.edge, ported.edge)
            and are_bound_ported_nodes_equal(bound.below, ported.below)
            and are_bound_ported_nodes_equal(bound.above, ported.above))


def point_to_coordinates(point: AnyPoint) -> Tuple[Coordinate, Coordinate]:
    return point.x, point.y


def sort_points(points_pair: Tuple[AnyPoint, AnyPoint]
                ) -> Tuple[AnyPoint, AnyPoint]:
    first, second = points_pair
    return (points_pair
            if second.is_right_of(first)
            else (second, first))


def are_endpoints_non_degenerate(endpoints: Tuple[BoundPortedPointsPair,
                                                  BoundPortedPointsPair]
                                 ) -> bool:
    (first_bound, _), (second_bound, _) = endpoints
    return first_bound != second_bound


def sort_endpoints(endpoints: Tuple[BoundPortedPointsPair,
                                    BoundPortedPointsPair]
                   ) -> Tuple[BoundPortedPointsPair, BoundPortedPointsPair]:
    (first_bound, _), (second_bound, _) = endpoints
    return (endpoints
            if second_bound.is_right_of(first_bound)
            else endpoints[::-1])


def is_edge_horizontal(edge: AnyEdge) -> bool:
    return edge.left.y == edge.right.y


def is_edge_vertical(edge: AnyEdge) -> bool:
    return edge.left.x == edge.right.x
