#include "edge.h"

#include <cassert>

Edge::Edge(const Point* left_, const Point* right_)
    : left(left_), right(right_) {
  assert(left != 0 && "Null left point");
  assert(right != 0 && "Null right point");
  assert(right->is_right_of(*left) && "Incorrect point order");
}

int Edge::get_point_orientation(const Point& xy) const {
  double cross_z = (xy - *left).cross_z(*right - *left);
  return (cross_z > 0.0) ? +1 : ((cross_z < 0.0) ? -1 : 0);
}

double Edge::get_slope() const {
  // Divide by zero is acceptable here.
  Point diff = *right - *left;
  return diff.y / diff.x;
}

double Edge::get_y_at_x(const double& x) const {
  if (left->x == right->x) {
    // If edge is vertical, return lowest y from left point.
    assert(x == left->x && "x outside of edge");
    return left->y;
  } else {
    // Equation of line: left + lambda*(right - left) = xy.
    // i.e. left.x + lambda(right.x - left.x) = x and similar for y.
    double lambda = (x - left->x) / (right->x - left->x);
    assert(lambda >= 0 && lambda <= 1.0 && "Lambda out of bounds");
    return left->y + lambda * (right->y - left->y);
  }
}

bool Edge::has_point(const Point* point) const {
  assert(point != 0 && "Null point");
  return (left == point || right == point);
}

bool Edge::operator==(const Edge& other) const { return this == &other; }
