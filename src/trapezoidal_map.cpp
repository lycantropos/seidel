#include "trapezoidal_map.h"

#include <algorithm>
#include <cassert>
#include <stdexcept>

#include "bounding_box.h"

/* Linear congruential random number generator.
 * Edges in the triangulation are randomly shuffled
 * before being added to the trapezoid map.
 * Want the shuffling to be identical across different operating systems
 * and the same regardless of previous random number use.
 * Would prefer to use a STL or Boost random number generator,
 * but support is not consistent across different operating systems
 * so implementing own here.
 *
 * This is not particularly random, but is perfectly adequate for the use here.
 * Coefficients taken from Numerical Recipes in C. */
class RandomNumberGenerator {
 public:
  RandomNumberGenerator(unsigned long seed)
      : _m(21870), _a(1291), _c(4621), _seed(seed % _m) {}

  // Return random integer in the range 0 to max_value-1.
  unsigned long operator()(unsigned long max_value) {
    _seed = (_seed * _a + _c) % _m;
    return (_seed * max_value) / _m;
  }

 private:
  const unsigned long _m, _a, _c;
  unsigned long _seed;
};

TrapezoidalMap::TrapezoidalMap(const std::vector<Point>& points)
    : npoints(points.size()), _points(points), _root(nullptr) {
  // Set up points array, which contains all of the points in the
  // triangulation plus the 4 corners of the enclosing rectangle.
  BoundingBox bbox;
  for (auto& xy : _points) {
    // Avoid problems with -0. values different from 0.
    if (xy.x == -0.) xy.x = 0.;
    if (xy.y == -0.) xy.y = 0.;
    bbox.add(xy);
  }

  // Last 4 points are corner points of enclosing rectangle.  Enclosing
  // rectangle made slightly larger in case corner points are already in the
  // triangulation.
  if (bbox.empty) {
    bbox.add(Point(0., 0.));
    bbox.add(Point(1., 1.));
  } else {
    const double small = 0.1;  // Any value > 0.
    bbox.expand((bbox.upper - bbox.lower) * small);
  }
  _points.push_back(Point(bbox.lower));                  // SW point.
  _points.push_back(Point(bbox.upper.x, bbox.lower.y));  // SE point.
  _points.push_back(Point(bbox.lower.x, bbox.upper.y));  // NW point.
  _points.push_back(Point(bbox.upper));                  // NE point.
}

TrapezoidalMap::~TrapezoidalMap() {
  _edges.clear();

  delete _root;
  _root = nullptr;
}

bool TrapezoidalMap::add_edge(const Edge& edge) {
  std::vector<Trapezoid*> trapezoids;
  if (!find_trapezoids_intersecting_edge(edge, trapezoids)) return false;
  assert(!trapezoids.empty() && "No trapezoids intersect edge");

  const Point* p = edge.left;
  const Point* q = edge.right;
  Trapezoid* left_old = nullptr;    // old trapezoid to the left.
  Trapezoid* left_below = nullptr;  // below trapezoid to the left.
  Trapezoid* left_above = nullptr;  // above trapezoid to the left.

  // Iterate through trapezoids intersecting edge from left to right.
  // Replace each old trapezoid with 2+ new trapezoids, and replace its
  // corresponding nodes in the search graph with new nodes.
  std::size_t ntraps = trapezoids.size();
  for (std::size_t i = 0; i < ntraps; ++i) {
    Trapezoid* old = trapezoids[i];  // old trapezoid to replace.
    bool start_trap = (i == 0);
    bool end_trap = (i == ntraps - 1);
    bool have_left = (start_trap && edge.left != old->left);
    bool have_right = (end_trap && edge.right != old->right);

    // Old trapezoid is replaced by up to 4 new trapezoids: left is to the
    // left of the start point p, below/above are below/above the edge
    // inserted, and right is to the right of the end point q.
    Trapezoid* left = nullptr;
    Trapezoid* below = nullptr;
    Trapezoid* above = nullptr;
    Trapezoid* right = nullptr;

    // There are 4 different cases here depending on whether the old
    // trapezoid in question is the start and/or end trapezoid of those
    // that intersect the edge inserted.  There is some code duplication
    // here but it is much easier to understand this way rather than
    // interleave the 4 different cases with many more if-statements.
    if (start_trap && end_trap) {
      // Edge intersects a single trapezoid.
      if (have_left) left = new Trapezoid(old->left, p, old->below, old->above);
      below = new Trapezoid(p, q, old->below, edge);
      above = new Trapezoid(p, q, edge, old->above);
      if (have_right)
        right = new Trapezoid(q, old->right, old->below, old->above);

      // Set pairs of trapezoid neighbours.
      if (have_left) {
        left->set_lower_left(old->lower_left);
        left->set_upper_left(old->upper_left);
        left->set_lower_right(below);
        left->set_upper_right(above);
      } else {
        below->set_lower_left(old->lower_left);
        above->set_upper_left(old->upper_left);
      }

      if (have_right) {
        right->set_lower_right(old->lower_right);
        right->set_upper_right(old->upper_right);
        below->set_lower_right(right);
        above->set_upper_right(right);
      } else {
        below->set_lower_right(old->lower_right);
        above->set_upper_right(old->upper_right);
      }
    } else if (start_trap) {
      // Old trapezoid is the first of 2+ trapezoids that the edge
      // intersects.
      if (have_left) left = new Trapezoid(old->left, p, old->below, old->above);
      below = new Trapezoid(p, old->right, old->below, edge);
      above = new Trapezoid(p, old->right, edge, old->above);

      // Set pairs of trapezoid neighbours.
      if (have_left) {
        left->set_lower_left(old->lower_left);
        left->set_upper_left(old->upper_left);
        left->set_lower_right(below);
        left->set_upper_right(above);
      } else {
        below->set_lower_left(old->lower_left);
        above->set_upper_left(old->upper_left);
      }

      below->set_lower_right(old->lower_right);
      above->set_upper_right(old->upper_right);
    } else if (end_trap) {
      // Old trapezoid is the last of 2+ trapezoids that the edge
      // intersects.
      if (left_below->below == old->below) {
        below = left_below;
        below->right = q;
      } else
        below = new Trapezoid(old->left, q, old->below, edge);

      if (left_above->above == old->above) {
        above = left_above;
        above->right = q;
      } else
        above = new Trapezoid(old->left, q, edge, old->above);

      if (have_right)
        right = new Trapezoid(q, old->right, old->below, old->above);

      // Set pairs of trapezoid neighbours.
      if (have_right) {
        right->set_lower_right(old->lower_right);
        right->set_upper_right(old->upper_right);
        below->set_lower_right(right);
        above->set_upper_right(right);
      } else {
        below->set_lower_right(old->lower_right);
        above->set_upper_right(old->upper_right);
      }

      // Connect to new trapezoids replacing prevOld.
      if (below != left_below) {
        below->set_upper_left(left_below);
        if (old->lower_left == left_old)
          below->set_lower_left(left_below);
        else
          below->set_lower_left(old->lower_left);
      }

      if (above != left_above) {
        above->set_lower_left(left_above);
        if (old->upper_left == left_old)
          above->set_upper_left(left_above);
        else
          above->set_upper_left(old->upper_left);
      }
    } else {  // Middle trapezoid.
      // Old trapezoid is neither the first nor last of the 3+ trapezoids
      // that the edge intersects.
      if (left_below->below == old->below) {
        below = left_below;
        below->right = old->right;
      } else
        below = new Trapezoid(old->left, old->right, old->below, edge);

      if (left_above->above == old->above) {
        above = left_above;
        above->right = old->right;
      } else
        above = new Trapezoid(old->left, old->right, edge, old->above);

      // Connect to new trapezoids replacing prevOld.
      if (below != left_below) {  // below is new.
        below->set_upper_left(left_below);
        if (old->lower_left == left_old)
          below->set_lower_left(left_below);
        else
          below->set_lower_left(old->lower_left);
      }

      if (above != left_above) {  // above is new.
        above->set_lower_left(left_above);
        if (old->upper_left == left_old)
          above->set_upper_left(left_above);
        else
          above->set_upper_left(old->upper_left);
      }

      below->set_lower_right(old->lower_right);
      above->set_upper_right(old->upper_right);
    }

    // Create new nodes to add to search graph.  Below and above trapezoids
    // may already have owning trapezoid nodes, in which case reuse them.
    Node* new_top_node = new Node(
        &edge, below == left_below ? below->trapezoid_node : new Node(below),
        above == left_above ? above->trapezoid_node : new Node(above));
    if (have_right) new_top_node = new Node(q, new_top_node, new Node(right));
    if (have_left) new_top_node = new Node(p, new Node(left), new_top_node);

    // Insert new_top_node in correct position or positions in search graph.
    Node* old_node = old->trapezoid_node;
    if (old_node == _root)
      _root = new_top_node;
    else
      old_node->replace_with(new_top_node);

    // old_node has been removed from all of its parents and is no longer
    // needed.
    assert(old_node->has_no_parents() && "Node should have no parents");
    delete old_node;

    // Clearing up.
    if (!end_trap) {
      // Prepare for next loop.
      left_old = old;
      left_above = above;
      left_below = below;
    }
  }

  return true;
}

bool TrapezoidalMap::find_trapezoids_intersecting_edge(
    const Edge& edge, std::vector<Trapezoid*>& trapezoids) {
  // This is the FollowSegment algorithm of de Berg et al, with some extra
  // checks to deal with simple collinear (i.e. invalid) triangles.
  trapezoids.clear();
  Trapezoid* trapezoid = _root->search(edge);
  if (trapezoid == nullptr) {
    assert(trapezoid != nullptr && "search(edge) returns null trapezoid");
    return false;
  }

  trapezoids.push_back(trapezoid);
  while (edge.right->is_right_of(*trapezoid->right)) {
    int orient = edge.get_point_orientation(*trapezoid->right);
    if (orient == 0) {
      assert(0 && "Unable to deal with point on edge");
      return false;
    }

    if (orient == -1)
      trapezoid = trapezoid->lower_right;
    else if (orient == +1)
      trapezoid = trapezoid->upper_right;

    if (trapezoid == nullptr) {
      assert(0 && "Expected trapezoid neighbor");
      return false;
    }
    trapezoids.push_back(trapezoid);
  }

  return true;
}

void TrapezoidalMap::build() {
  // Set up edges array.
  // First the bottom and top edges of the enclosing rectangle.
  _edges.push_back(Edge(&_points[npoints], &_points[npoints + 1]));
  _edges.push_back(Edge(&_points[npoints + 2], &_points[npoints + 3]));

  for (std::size_t index = 0; index < npoints; ++index) {
    Point* start = &_points[index];
    Point* end = &_points[(index + 1) % npoints];
    if (end->is_right_of(*start))
      _edges.push_back(Edge(start, end));
    else
      _edges.push_back(Edge(end, start));
  }

  // Initial trapezoid is enclosing rectangle.
  _root = new Node(new Trapezoid(&_points[npoints], &_points[npoints + 1],
                                 _edges[0], _edges[1]));
  _root->assert_valid();

  // Randomly shuffle all edges other than first 2.
  RandomNumberGenerator rng(1234);
  std::random_shuffle(_edges.begin() + 2, _edges.end(), rng);

  // Add edges, one at a time, to graph.
  std::size_t nedges = _edges.size();
  for (std::size_t index = 2; index < nedges; ++index) {
    if (!add_edge(_edges[index]))
      throw std::runtime_error("Triangulation is invalid");
    _root->assert_valid();
  }
}
