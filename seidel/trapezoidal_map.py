import random
from typing import (List,
                    Sequence)

from .bounding_box import BoundingBox
from .edge import Edge
from .leaf import Leaf
from .node import Node
from .point import Point
from .trapezoid import Trapezoid
from .x_node import XNode
from .y_node import YNode


def build_graph(points: Sequence[Point], shuffle: bool) -> Node:
    bounding_box = BoundingBox(True, Point(0, 0), Point(0, 0))
    points = list(points)
    points_count = len(points)
    for point in points:
        if not point.x:
            point.x = 0
        if not point.y:
            point.y = 0
        bounding_box.add(point)
    # Last 4 points are corner points of enclosing rectangle.  Enclosing
    # rectangle made slightly larger in case corner points are already in the
    # triangulation.
    if bounding_box.empty:
        bounding_box.add(Point(0., 0.))
        bounding_box.add(Point(1., 1.))
    else:
        small = 0.1  # Any value > 0.
        bounding_box.expand((bounding_box.upper - bounding_box.lower) * small)
    # SW point.
    points.append(bounding_box.lower)
    # SE point.
    points.append(Point(bounding_box.upper.x, bounding_box.lower.y))
    # NW point.
    points.append(Point(bounding_box.lower.x, bounding_box.upper.y))
    # NE point.
    points.append(bounding_box.upper)

    edges = [Edge(points[points_count], points[points_count + 1]),
             Edge(points[points_count + 2], points[points_count + 3])]
    for index in range(points_count):
        start, end = points[index], points[(index + 1) % points_count]
        edges.append(Edge(start, end)
                     if end.is_right_of(start)
                     else Edge(end, start))
    if shuffle:
        random.shuffle(edges)
    result = Leaf(Trapezoid(points[points_count], points[points_count + 1],
                            edges[0], edges[1]))
    for index in range(2, len(edges)):
        result = add_edge_to_graph(result, edges[index])
    return result


def add_edge_to_graph(graph: Node, edge: Edge) -> Node:
    trapezoids = find_trapezoids_intersecting_edge(graph, edge)
    p = edge.left
    q = edge.right
    left_old = None  # old trapezoid to the left.
    left_below = None  # below trapezoid to the left.
    left_above = None  # above trapezoid to the left.
    for index, old in enumerate(trapezoids):
        start_trap = index == 0
        end_trap = index == len(trapezoids) - 1
        have_left = start_trap and edge.left != old.left
        have_right = end_trap and edge.right != old.right
        left = right = None
        if start_trap and end_trap:
            if have_left:
                left = Trapezoid(old.left, p, old.below, old.above)
            below = Trapezoid(p, q, old.below, edge)
            above = Trapezoid(p, q, edge, old.above)
            if have_right:
                right = Trapezoid(q, old.right, old.below, old.above)
            if have_left:
                left.lower_left = old.lower_left
                left.upper_left = old.upper_left
                left.lower_right = below
                left.upper_right = above
            else:
                below.lower_left = old.lower_left
                above.upper_left = old.upper_left
            if have_right:
                right.lower_right = old.lower_right
                right.upper_right = old.upper_right
                below.lower_right = right
                above.upper_right = right
            else:
                below.lower_right = old.lower_right
                above.upper_right = old.upper_right
        elif start_trap:
            # Old trapezoid is the first of 2+ trapezoids
            # that the edge intersects.
            if have_left:
                left = Trapezoid(old.left, p, old.below, old.above)
            below = Trapezoid(p, old.right, old.below, edge)
            above = Trapezoid(p, old.right, edge, old.above)

            # Set pairs of trapezoid neighbours.
            if have_left:
                left.lower_left = old.lower_left
                left.upper_left = old.upper_left
                left.lower_right = below
                left.upper_right = above
            else:
                below.lower_left = old.lower_left
                above.upper_left = old.upper_left
            below.lower_right = old.lower_right
            above.upper_right = old.upper_right
        elif end_trap:
            # Old trapezoid is the last of 2+ trapezoids that the edge
            # intersects.
            if left_below.below == old.below:
                below = left_below
                below.right = q
            else:
                below = Trapezoid(old.left, q, old.below, edge)

            if left_above.above == old.above:
                above = left_above
                above.right = q
            else:
                above = Trapezoid(old.left, q, edge, old.above)

            if have_right:
                right = Trapezoid(q, old.right, old.below, old.above)

            # Set pairs of trapezoid neighbours.
            if have_right:
                right.lower_right = old.lower_right
                right.upper_right = old.upper_right
                below.lower_right = right
                above.upper_right = right
            else:
                below.lower_right = old.lower_right
                above.upper_right = old.upper_right

            # Connect to new trapezoids replacing old.
            if below != left_below:
                below.upper_left = left_below
                below.lower_left = (left_below
                                    if old.lower_left is left_old
                                    else old.lower_left)

            if above != left_above:
                above.lower_left = left_above
                above.upper_left = (left_above
                                    if old.upper_left is left_old
                                    else old.upper_left)
        else:
            # Middle trapezoid.
            # Old trapezoid is neither the first nor last of the 3+ trapezoids
            # that the edge intersects.
            if left_below.below == old.below:
                below = left_below
                below.right = old.right
            else:
                below = Trapezoid(old.left, old.right, old.below, edge)

            if left_above.above == old.above:
                above = left_above
                above.right = old.right
            else:
                above = Trapezoid(old.left, old.right, edge, old.above)

            # Connect to new trapezoids replacing prevOld.
            if below != left_below:  # below is new.
                below.upper_left = left_below
                below.lower_left = (left_below
                                    if old.lower_left is left_old
                                    else old.lower_left)

            if above != left_above:  # above is new.
                above.lower_left = left_above
                above.upper_left = (left_above
                                    if old.upper_left is left_old
                                    else old.upper_left)
            below.lower_right = old.lower_right
            above.upper_right = old.upper_right
        new_top_node = YNode(edge,
                             below.trapezoid_node
                             if below == left_below
                             else Leaf(below),
                             above.trapezoid_node
                             if above == left_above
                             else Leaf(above))
        if have_right:
            new_top_node = XNode(q, new_top_node, Leaf(right))
        if have_left:
            new_top_node = XNode(p, Leaf(left), new_top_node)
        old_node = old.trapezoid_node
        if old_node is graph:
            graph = new_top_node
        else:
            old_node.replace_with(new_top_node)
        if not end_trap:
            # Prepare for next loop.
            left_old = old
            left_above = above
            left_below = below
    return graph


def find_trapezoids_intersecting_edge(graph: Node,
                                      edge: Edge) -> List[Trapezoid]:
    trapezoid = graph.search_edge(edge)
    result = [trapezoid]
    while edge.right.is_right_of(trapezoid.right):
        orient = edge.orientation_with(trapezoid.right)
        assert orient, 'Unable to deal with point on edge.'
        if orient == -1:
            trapezoid = trapezoid.lower_right
        elif orient == 1:
            trapezoid = trapezoid.upper_right
        assert trapezoid is not None, ('Expected neighbour trapezoid, '
                                       'but none found.')
        result.append(trapezoid)
    return result
