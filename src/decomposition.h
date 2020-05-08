#ifndef DECOMPOSITION_H
#define DECOMPOSITION_H

#include <iostream>
#include <list>
#include <map>
#include <set>
#include <vector>

#include "edge.h"
#include "node.h"
#include "point.h"
#include "trapezoid.h"

/* Implemented using the trapezoid map algorithm from the book
 * "Computational Geometry, Algorithms and Applications", second edition,
 * by M. de Berg, M. van Kreveld, M. Overmars and O. Schwarzkopf.
 *
 * The domain of interest is composed of vertical-sided trapezoids that are
 * bounded to the left and right by points of the triangulation, and below and
 * above by edges of the triangulation.  Each triangle is represented by 1 or
 * more of these trapezoids.  Edges are inserted one a time in a random order.
 *
 * As the trapezoid map is created, a search tree is also created which allows
 * fast lookup O(log N) of the trapezoid containing the point of interest.
 * There are 3 types of node in the search tree: all leaf nodes represent
 * trapezoids and all branch nodes have 2 child nodes and are either x-nodes or
 * y-nodes.  X-nodes represent points in the triangulation, and their 2 children
 * refer to those parts of the search tree to the left and right of the point.
 * Y-nodes represent edges in the triangulation, and their 2 children refer to
 * those parts of the search tree below and above the edge.
 *
 * Nodes can be repeated throughout the search tree, and each is reference
 * counted through the multiple parent nodes it is a child of.
 *
 * The algorithm is only intended to work with valid decompositions, i.e. it
 * must not contain duplicate points, triangles formed from collinear points,
 * or overlapping triangles.  It does have some tolerance to triangles
 * formed from collinear points but only in the simplest of cases.
 * No explicit testing of the validity of the triangulation is performed
 * as this is a computationally more complex task than the trifinding itself.
 */
class TrapezoidalMap {
 public:
  /* Constructor.  A separate call to initialize() is required to initialize
   * the object before use.
   */
  TrapezoidalMap(const std::vector<Point>&);

  ~TrapezoidalMap();

  NodeStats get_tree_stats();

  /* Initialize this object before use.  May be called multiple times, if,
   * for example, the triangulation is changed by setting the mask. */
  void initialize();

  // Print the search tree as text to stdout; useful for debug purposes.
  void print_tree();

 private:
  // Add the specified Edge to the search tree, returning true if successful.
  bool add_edge_to_tree(const Edge& edge);

  // Clear all memory allocated by this object.
  void clear();

  /* Determine the trapezoids that the specified Edge intersects, returning
   * true if successful. */
  bool find_trapezoids_intersecting_edge(const Edge& edge,
                                         std::vector<Trapezoid*>& trapezoids);

  size_t npoints;
  // All points plus corners of enclosing rectangle.
  std::vector<Point> _points;
  // All edges plus bottom and top edges of enclosing rectangle.
  Edges _edges;
  // Root node of the trapezoid map search tree, owned.
  Node* _tree;
};

/* Linear congruential random number generator.  Edges in the triangulation are
 * randomly shuffled before being added to the trapezoid map.  Want the
 * shuffling to be identical across different operating systems and the same
 * regardless of previous random number use.  Would prefer to use a STL or
 * Boost random number generator, but support is not consistent across
 * different operating systems so implementing own here.
 *
 * This is not particularly random, but is perfectly adequate for the use here.
 * Coefficients taken from Numerical Recipes in C. */
class RandomNumberGenerator {
 public:
  RandomNumberGenerator(unsigned long seed);

  // Return random integer in the range 0 to max_value-1.
  unsigned long operator()(unsigned long max_value);

 private:
  const unsigned long _m, _a, _c;
  unsigned long _seed;
};

#endif
