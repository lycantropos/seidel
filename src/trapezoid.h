#ifndef TRAPEZOID_H
#define TRAPEZOID_H

#include "edge.h"
#include "point.h"

class Node;  // Forward declaration.

/* A Trapezoid is bounded by Points to left and right, and Edges below and
 * above.  Has up to 4 neighboring Trapezoids to lower/upper left/right.
 * Lower left neighbor is Trapezoid to left that shares the below Edge, or
 * is 0 if there is no such Trapezoid (and similar for other neighbors).
 * To obtain the index of the triangle corresponding to a particular
 * Trapezoid, use the Edge member variables below.triangle_above or
 * above.triangle_below. */
struct Trapezoid {
  Trapezoid(const Point* left_, const Point* right_, const Edge& below_,
            const Edge& above_);

  /* Assert that this Trapezoid is valid.  Reduces to a no-op if NDEBUG
   * is defined. */
  void assert_valid(bool tree_complete) const;

  /* Return one of the 4 corner points of this Trapezoid.  Only used for
   * debugging purposes. */
  Point get_lower_left_point() const;
  Point get_lower_right_point() const;
  Point get_upper_left_point() const;
  Point get_upper_right_point() const;

  void print_debug() const;

  /* Set one of the 4 neighbor trapezoids and the corresponding reverse
   * Trapezoid of the new neighbor (if it is not 0), so that they are
   * consistent. */
  void set_lower_left(Trapezoid* lower_left_);
  void set_lower_right(Trapezoid* lower_right_);
  void set_upper_left(Trapezoid* upper_left_);
  void set_upper_right(Trapezoid* upper_right_);

  /* Copy constructor and assignment operator defined but not implemented
   * to prevent objects being copied. */
  Trapezoid(const Trapezoid& other);
  Trapezoid& operator=(const Trapezoid& other);

  const Point* left;   // Not owned.
  const Point* right;  // Not owned.
  const Edge& below;
  const Edge& above;

  // 4 neighboring trapezoids, can be 0, not owned.
  Trapezoid* lower_left;   // Trapezoid to left  that shares below
  Trapezoid* lower_right;  // Trapezoid to right that shares below
  Trapezoid* upper_left;   // Trapezoid to left  that shares above
  Trapezoid* upper_right;  // Trapezoid to right that shares above

  Node* trapezoid_node;  // Node that owns this Trapezoid.
};

#endif