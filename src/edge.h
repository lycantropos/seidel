#ifndef EDGE_H
#define EDGE_H

#include <iostream>
#include <vector>

#include "point.h"

/* An Edge connects two Points, left and right.
 * It is always true that right->is_right_of(*left).
 */
struct Edge {
  Edge(const Point* left_, const Point* right_);

  // Return -1 if point to left of edge, 0 if on edge, +1 if to right.
  int get_point_orientation(const Point& xy) const;

  // Return slope of edge, even if vertical (divide by zero is OK here).
  double get_slope() const;

  /* Return y-coordinate of point on edge with specified x-coordinate.
   * x must be within the x-limits of this edge. */
  double get_y_at_x(const double& x) const;

  // Return true if the specified point is either of the edge end points.
  bool has_point(const Point* point) const;

  bool operator==(const Edge& other) const;

  friend std::ostream& operator<<(std::ostream& os, const Edge& edge) {
    return os << *edge.left << "->" << *edge.right;
  }

  void print_debug() const;

  const Point* left;         // Not owned.
  const Point* right;        // Not owned.
  const Point* point_below;  // Used only for resolving ambiguous cases;
  const Point* point_above;  //     is 0 if corresponding triangle is -1
};

typedef std::vector<Edge> Edges;

#endif
