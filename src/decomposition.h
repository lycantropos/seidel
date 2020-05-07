#ifndef DECOMPOSITION_H
#define DECOMPOSITION_H

#include <iostream>
#include <list>
#include <map>
#include <set>
#include <vector>

#include "point.h"

/* An Edge connects two Points, left and right.  It is always true that
 * right->is_right_of(*left).  Stores indices of triangles below and above
 * the Edge which are used to map from trapezoid to triangle index.  Also
 * stores pointers to the 3rd points of the below and above triangles,
 * which are only used to disambiguate triangles with colinear points. */
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

class Node;  // Forward declaration.

// Helper structure used by TrapezoidMap::get_tree_stats.
struct NodeStats {
  NodeStats()
      : node_count(0),
        trapezoid_count(0),
        max_parent_count(0),
        max_depth(0),
        sum_trapezoid_depth(0.0) {}

  long node_count, trapezoid_count, max_parent_count, max_depth;
  double sum_trapezoid_depth;
  std::set<const Node*> unique_nodes, unique_trapezoid_nodes;
};

struct Trapezoid;  // Forward declaration.

/* Node of the trapezoid map search tree.  There are 3 possible types:
 * Type_XNode, Type_YNode and Type_TrapezoidNode.  Data members are
 * represented using a union: an XNode has a Point and 2 child nodes
 * (left and right of the point), a YNode has an Edge and 2 child nodes
 * (below and above the edge), and a TrapezoidNode has a Trapezoid.
 * Each Node has multiple parents so it can appear in the search tree
 * multiple times without having to create duplicate identical Nodes.
 * The parent collection acts as a reference count to the number of times
 * a Node occurs in the search tree.  When the parent count is reduced to
 * zero a Node can be safely deleted. */
class Node {
 public:
  Node(const Point* point, Node* left, Node* right);  // Type_XNode.
  Node(const Edge* edge, Node* below, Node* above);   // Type_YNode.
  Node(Trapezoid* trapezoid);                         // Type_TrapezoidNode.

  ~Node();

  void add_parent(Node* parent);

  /* Recurse through the search tree and assert that everything is valid.
   * Reduces to a no-op if NDEBUG is defined. */
  void assert_valid(bool tree_complete) const;

  // Recurse through the tree to return statistics about it.
  void get_stats(int depth, NodeStats& stats) const;

  bool has_child(const Node* child) const;
  bool has_no_parents() const;
  bool has_parent(const Node* parent) const;

  /* Recurse through the tree and print a textual representation to
   * stdout.  Argument depth used to indent for readability. */
  void print(int depth = 0) const;

  /* Remove a parent from this Node.  Return true if no parents remain
   * so that this Node can be deleted. */
  bool remove_parent(Node* parent);

  void replace_child(Node* old_child, Node* new_child);

  // Replace this node with the specified new_node in all parents.
  void replace_with(Node* new_node);

  /* Recursive search through the tree to find the Node containing the
   * specified Point point. */
  const Node* search(const Point& xy);

  /* Recursive search through the tree to find the Trapezoid containing
   * the left endpoint of the specified Edge.  Return 0 if fails, which
   * can only happen if the triangulation is invalid. */
  Trapezoid* search(const Edge& edge);

  /* Copy constructor and assignment operator defined but not implemented
   * to prevent objects being copied. */
  Node(const Node& other);
  Node& operator=(const Node& other);

 private:
  typedef enum { Type_XNode, Type_YNode, Type_TrapezoidNode } Type;
  Type _type;

  union {
    struct {
      const Point* point;  // Not owned.
      Node* left;          // Owned.
      Node* right;         // Owned.
    } xnode;
    struct {
      const Edge* edge;  // Not owned.
      Node* below;       // Owned.
      Node* above;       // Owned.
    } ynode;
    Trapezoid* trapezoid;  // Owned.
  } _union;

  typedef std::list<Node*> Parents;
  Parents _parents;  // Not owned.
};

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
class TrapezoidMap {
 public:
  /* Constructor.  A separate call to initialize() is required to initialize
   * the object before use.
   */
  TrapezoidMap(const std::vector<Point>&);

  ~TrapezoidMap();

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
