#include "decomposition.h"

#include <algorithm>
#include <cassert>
#include <set>

Point::Point() {}

Point::Point(const double& x_, const double& y_) : x(x_), y(y_) {}

double Point::angle() const { return atan2(y, x); }

double Point::cross_z(const Point& other) const {
  return x * other.y - y * other.x;
}

bool Point::is_right_of(const Point& other) const {
  if (x == other.x)
    return y > other.y;
  else
    return x > other.x;
}

bool Point::operator==(const Point& other) const {
  return x == other.x && y == other.y;
}

bool Point::operator!=(const Point& other) const {
  return x != other.x || y != other.y;
}

Point Point::operator*(const double& multiplier) const {
  return Point(x * multiplier, y * multiplier);
}

const Point& Point::operator+=(const Point& other) {
  x += other.x;
  y += other.y;
  return *this;
}

const Point& Point::operator-=(const Point& other) {
  x -= other.x;
  y -= other.y;
  return *this;
}

Point Point::operator+(const Point& other) const {
  return Point(x + other.x, y + other.y);
}

Point Point::operator-(const Point& other) const {
  return Point(x - other.x, y - other.y);
}

std::ostream& operator<<(std::ostream& os, const Point& xy) {
  return os << '(' << xy.x << ' ' << xy.y << ')';
}

BoundingBox::BoundingBox() : empty(true), lower(0.0, 0.0), upper(0.0, 0.0) {}

void BoundingBox::add(const Point& point) {
  if (empty) {
    empty = false;
    lower = upper = point;
  } else {
    if (point.x < lower.x)
      lower.x = point.x;
    else if (point.x > upper.x)
      upper.x = point.x;

    if (point.y < lower.y)
      lower.y = point.y;
    else if (point.y > upper.y)
      upper.y = point.y;
  }
}

void BoundingBox::expand(const Point& delta) {
  if (!empty) {
    lower -= delta;
    upper += delta;
  }
}

TrapezoidMap::TrapezoidMap(const std::vector<Point>& points)
    : _points(points), npoints(points.size()), _tree(nullptr) {
  clear();
  // Set up points array, which contains all of the points in the
  // triangulation plus the 4 corners of the enclosing rectangle.
  BoundingBox bbox;
  for (auto& xy : _points) {
    // Avoid problems with -0.0 values different from 0.0
    if (xy.x == -0.0) xy.x = 0.0;
    if (xy.y == -0.0) xy.y = 0.0;
    bbox.add(xy);
  }

  // Last 4 points are corner points of enclosing rectangle.  Enclosing
  // rectangle made slightly larger in case corner points are already in the
  // triangulation.
  if (bbox.empty) {
    bbox.add(Point(0.0, 0.0));
    bbox.add(Point(1.0, 1.0));
  } else {
    const double small = 0.1;  // Any value > 0.0
    bbox.expand((bbox.upper - bbox.lower) * small);
  }
  _points.push_back(Point(bbox.lower));                  // SW point.
  _points.push_back(Point(bbox.upper.x, bbox.lower.y));  // SE point.
  _points.push_back(Point(bbox.lower.x, bbox.upper.y));  // NW point.
  _points.push_back(Point(bbox.upper));                  // NE point.
}

TrapezoidMap::~TrapezoidMap() { clear(); }

bool TrapezoidMap::add_edge_to_tree(const Edge& edge) {
  std::vector<Trapezoid*> trapezoids;
  if (!find_trapezoids_intersecting_edge(edge, trapezoids)) return false;
  assert(!trapezoids.empty() && "No trapezoids intersect edge");

  const Point* p = edge.left;
  const Point* q = edge.right;
  Trapezoid* left_old = 0;    // old trapezoid to the left.
  Trapezoid* left_below = 0;  // below trapezoid to the left.
  Trapezoid* left_above = 0;  // above trapezoid to the left.

  // Iterate through trapezoids intersecting edge from left to right.
  // Replace each old trapezoid with 2+ new trapezoids, and replace its
  // corresponding nodes in the search tree with new nodes.
  size_t ntraps = trapezoids.size();
  for (size_t i = 0; i < ntraps; ++i) {
    Trapezoid* old = trapezoids[i];  // old trapezoid to replace.
    bool start_trap = (i == 0);
    bool end_trap = (i == ntraps - 1);
    bool have_left = (start_trap && edge.left != old->left);
    bool have_right = (end_trap && edge.right != old->right);

    // Old trapezoid is replaced by up to 4 new trapezoids: left is to the
    // left of the start point p, below/above are below/above the edge
    // inserted, and right is to the right of the end point q.
    Trapezoid* left = 0;
    Trapezoid* below = 0;
    Trapezoid* above = 0;
    Trapezoid* right = 0;

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

    // Create new nodes to add to search tree.  Below and above trapezoids
    // may already have owning trapezoid nodes, in which case reuse them.
    Node* new_top_node = new Node(
        &edge, below == left_below ? below->trapezoid_node : new Node(below),
        above == left_above ? above->trapezoid_node : new Node(above));
    if (have_right) new_top_node = new Node(q, new_top_node, new Node(right));
    if (have_left) new_top_node = new Node(p, new Node(left), new_top_node);

    // Insert new_top_node in correct position or positions in search tree.
    Node* old_node = old->trapezoid_node;
    if (old_node == _tree)
      _tree = new_top_node;
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

void TrapezoidMap::clear() {
  _points.clear();

  _edges.clear();

  delete _tree;
  _tree = nullptr;
}

bool TrapezoidMap::find_trapezoids_intersecting_edge(
    const Edge& edge, std::vector<Trapezoid*>& trapezoids) {
  // This is the FollowSegment algorithm of de Berg et al, with some extra
  // checks to deal with simple colinear (i.e. invalid) triangles.
  trapezoids.clear();
  Trapezoid* trapezoid = _tree->search(edge);
  if (trapezoid == 0) {
    assert(trapezoid != 0 && "search(edge) returns null trapezoid");
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

    if (trapezoid == 0) {
      assert(0 && "Expected trapezoid neighbor");
      return false;
    }
    trapezoids.push_back(trapezoid);
  }

  return true;
}

NodeStats TrapezoidMap::get_tree_stats() {
  NodeStats stats;
  _tree->get_stats(0, stats);
  return stats;
}

void TrapezoidMap::initialize() {
  // Set up edges array.
  // First the bottom and top edges of the enclosing rectangle.
  _edges.push_back(Edge(&_points[npoints], &_points[npoints + 1]));
  _edges.push_back(Edge(&_points[npoints + 2], &_points[npoints + 3]));

  // Add all edges in the triangulation that point to the right.  Do not
  // explicitly include edges that point to the left as the neighboring
  // triangle will supply that, unless there is no such neighbor.
  for (size_t index = 0; index < npoints; ++index) {
    Point* start = &_points[index];
    Point* end = &_points[(index + 1) % npoints];
    if (end->is_right_of(*start))
      _edges.push_back(Edge(start, end));
    else
      _edges.push_back(Edge(end, start));
  }

  // Initial trapezoid is enclosing rectangle.
  _tree = new Node(new Trapezoid(&_points[npoints], &_points[npoints + 1],
                                 _edges[0], _edges[1]));
  _tree->assert_valid(false);

  // Randomly shuffle all edges other than first 2.
  RandomNumberGenerator rng(1234);
  std::random_shuffle(_edges.begin() + 2, _edges.end(), rng);

  // Add edges, one at a time, to tree.
  size_t nedges = _edges.size();
  for (size_t index = 2; index < nedges; ++index) {
    if (!add_edge_to_tree(_edges[index]))
      throw std::runtime_error("Triangulation is invalid");
    _tree->assert_valid(index == nedges - 1);
  }
}

void TrapezoidMap::print_tree() {
  assert(_tree != 0 && "Null Node tree");
  _tree->print();
}

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

void Edge::print_debug() const { std::cout << "Edge " << *this << std::endl; }

Node::Node(const Point* point, Node* left, Node* right) : _type(Type_XNode) {
  assert(point != 0 && "Invalid point");
  assert(left != 0 && "Invalid left node");
  assert(right != 0 && "Invalid right node");
  _union.xnode.point = point;
  _union.xnode.left = left;
  _union.xnode.right = right;
  left->add_parent(this);
  right->add_parent(this);
}

Node::Node(const Edge* edge, Node* below, Node* above) : _type(Type_YNode) {
  assert(edge != 0 && "Invalid edge");
  assert(below != 0 && "Invalid below node");
  assert(above != 0 && "Invalid above node");
  _union.ynode.edge = edge;
  _union.ynode.below = below;
  _union.ynode.above = above;
  below->add_parent(this);
  above->add_parent(this);
}

Node::Node(Trapezoid* trapezoid) : _type(Type_TrapezoidNode) {
  assert(trapezoid != 0 && "Null Trapezoid");
  _union.trapezoid = trapezoid;
  trapezoid->trapezoid_node = this;
}

Node::~Node() {
  switch (_type) {
    case Type_XNode:
      if (_union.xnode.left->remove_parent(this)) delete _union.xnode.left;
      if (_union.xnode.right->remove_parent(this)) delete _union.xnode.right;
      break;
    case Type_YNode:
      if (_union.ynode.below->remove_parent(this)) delete _union.ynode.below;
      if (_union.ynode.above->remove_parent(this)) delete _union.ynode.above;
      break;
    case Type_TrapezoidNode:
      delete _union.trapezoid;
      break;
  }
}

void Node::add_parent(Node* parent) {
  assert(parent != 0 && "Null parent");
  assert(parent != this && "Cannot be parent of self");
  assert(!has_parent(parent) && "Parent already in collection");
  _parents.push_back(parent);
}

void Node::assert_valid(bool tree_complete) const {
#ifndef NDEBUG
  // Check parents.
  for (Parents::const_iterator it = _parents.begin(); it != _parents.end();
       ++it) {
    Node* parent = *it;
    assert(parent != this && "Cannot be parent of self");
    assert(parent->has_child(this) && "Parent missing child");
  }

  // Check children, and recurse.
  switch (_type) {
    case Type_XNode:
      assert(_union.xnode.left != 0 && "Null left child");
      assert(_union.xnode.left->has_parent(this) && "Incorrect parent");
      assert(_union.xnode.right != 0 && "Null right child");
      assert(_union.xnode.right->has_parent(this) && "Incorrect parent");
      _union.xnode.left->assert_valid(tree_complete);
      _union.xnode.right->assert_valid(tree_complete);
      break;
    case Type_YNode:
      assert(_union.ynode.below != 0 && "Null below child");
      assert(_union.ynode.below->has_parent(this) && "Incorrect parent");
      assert(_union.ynode.above != 0 && "Null above child");
      assert(_union.ynode.above->has_parent(this) && "Incorrect parent");
      _union.ynode.below->assert_valid(tree_complete);
      _union.ynode.above->assert_valid(tree_complete);
      break;
    case Type_TrapezoidNode:
      assert(_union.trapezoid != 0 && "Null trapezoid");
      assert(_union.trapezoid->trapezoid_node == this &&
             "Incorrect trapezoid node");
      _union.trapezoid->assert_valid(tree_complete);
      break;
  }
#endif
}

void Node::get_stats(int depth, NodeStats& stats) const {
  stats.node_count++;
  if (depth > stats.max_depth) stats.max_depth = depth;
  bool new_node = stats.unique_nodes.insert(this).second;
  if (new_node)
    stats.max_parent_count =
        std::max(stats.max_parent_count, static_cast<long>(_parents.size()));

  switch (_type) {
    case Type_XNode:
      _union.xnode.left->get_stats(depth + 1, stats);
      _union.xnode.right->get_stats(depth + 1, stats);
      break;
    case Type_YNode:
      _union.ynode.below->get_stats(depth + 1, stats);
      _union.ynode.above->get_stats(depth + 1, stats);
      break;
    default:  // Type_TrapezoidNode:
      stats.unique_trapezoid_nodes.insert(this);
      stats.trapezoid_count++;
      stats.sum_trapezoid_depth += depth;
      break;
  }
}

bool Node::has_child(const Node* child) const {
  assert(child != 0 && "Null child node");
  switch (_type) {
    case Type_XNode:
      return (_union.xnode.left == child || _union.xnode.right == child);
    case Type_YNode:
      return (_union.ynode.below == child || _union.ynode.above == child);
    default:  // Type_TrapezoidNode:
      return false;
  }
}

bool Node::has_no_parents() const { return _parents.empty(); }

bool Node::has_parent(const Node* parent) const {
  return (std::find(_parents.begin(), _parents.end(), parent) !=
          _parents.end());
}

void Node::print(int depth /* = 0 */) const {
  for (int i = 0; i < depth; ++i) std::cout << "  ";
  switch (_type) {
    case Type_XNode:
      std::cout << "XNode " << *_union.xnode.point << std::endl;
      _union.xnode.left->print(depth + 1);
      _union.xnode.right->print(depth + 1);
      break;
    case Type_YNode:
      std::cout << "YNode " << *_union.ynode.edge << std::endl;
      _union.ynode.below->print(depth + 1);
      _union.ynode.above->print(depth + 1);
      break;
    case Type_TrapezoidNode:
      std::cout << "Trapezoid ll=" << _union.trapezoid->get_lower_left_point()
                << " lr=" << _union.trapezoid->get_lower_right_point()
                << " ul=" << _union.trapezoid->get_upper_left_point()
                << " ur=" << _union.trapezoid->get_upper_right_point()
                << std::endl;
      break;
  }
}

bool Node::remove_parent(Node* parent) {
  assert(parent != 0 && "Null parent");
  assert(parent != this && "Cannot be parent of self");
  Parents::iterator it = std::find(_parents.begin(), _parents.end(), parent);
  assert(it != _parents.end() && "Parent not in collection");
  _parents.erase(it);
  return _parents.empty();
}

void Node::replace_child(Node* old_child, Node* new_child) {
  switch (_type) {
    case Type_XNode:
      assert(
          (_union.xnode.left == old_child || _union.xnode.right == old_child) &&
          "Not a child Node");
      assert(new_child != 0 && "Null child node");
      if (_union.xnode.left == old_child)
        _union.xnode.left = new_child;
      else
        _union.xnode.right = new_child;
      break;
    case Type_YNode:
      assert((_union.ynode.below == old_child ||
              _union.ynode.above == old_child) &&
             "Not a child node");
      assert(new_child != 0 && "Null child node");
      if (_union.ynode.below == old_child)
        _union.ynode.below = new_child;
      else
        _union.ynode.above = new_child;
      break;
    case Type_TrapezoidNode:
      assert(0 && "Invalid type for this operation");
      break;
  }
  old_child->remove_parent(this);
  new_child->add_parent(this);
}

void Node::replace_with(Node* new_node) {
  assert(new_node != 0 && "Null replacement node");
  // Replace child of each parent with new_node.  As each has parent has its
  // child replaced it is removed from the _parents collection.
  while (!_parents.empty()) _parents.front()->replace_child(this, new_node);
}

const Node* Node::search(const Point& xy) {
  switch (_type) {
    case Type_XNode:
      if (xy == *_union.xnode.point)
        return this;
      else if (xy.is_right_of(*_union.xnode.point))
        return _union.xnode.right->search(xy);
      else
        return _union.xnode.left->search(xy);
    case Type_YNode: {
      int orient = _union.ynode.edge->get_point_orientation(xy);
      if (orient == 0)
        return this;
      else if (orient < 0)
        return _union.ynode.above->search(xy);
      else
        return _union.ynode.below->search(xy);
    }
    default:  // Type_TrapezoidNode:
      return this;
  }
}

Trapezoid* Node::search(const Edge& edge) {
  switch (_type) {
    case Type_XNode:
      if (edge.left == _union.xnode.point)
        return _union.xnode.right->search(edge);
      else {
        if (edge.left->is_right_of(*_union.xnode.point))
          return _union.xnode.right->search(edge);
        else
          return _union.xnode.left->search(edge);
      }
    case Type_YNode:
      if (edge.left == _union.ynode.edge->left) {
        // Coinciding left edge points.
        if (edge.get_slope() == _union.ynode.edge->get_slope()) {
          assert(0 && "Invalid triangulation, common left points");
          return 0;
        }
        if (edge.get_slope() > _union.ynode.edge->get_slope())
          return _union.ynode.above->search(edge);
        else
          return _union.ynode.below->search(edge);
      } else if (edge.right == _union.ynode.edge->right) {
        // Coinciding right edge points.
        if (edge.get_slope() == _union.ynode.edge->get_slope()) {
          assert(0 && "Invalid triangulation, common right points");
          return 0;
        }
        if (edge.get_slope() > _union.ynode.edge->get_slope())
          return _union.ynode.below->search(edge);
        else
          return _union.ynode.above->search(edge);
      } else {
        int orient = _union.ynode.edge->get_point_orientation(*edge.left);
        if (orient == 0) {
          assert(0 && "Invalid triangulation, point on edge");
          return 0;
        }
        if (orient < 0)
          return _union.ynode.above->search(edge);
        else
          return _union.ynode.below->search(edge);
      }
    default:  // Type_TrapezoidNode:
      return _union.trapezoid;
  }
}

Trapezoid::Trapezoid(const Point* left_, const Point* right_,
                     const Edge& below_, const Edge& above_)
    : left(left_),
      right(right_),
      below(below_),
      above(above_),
      lower_left(0),
      lower_right(0),
      upper_left(0),
      upper_right(0),
      trapezoid_node(0) {
  assert(left != 0 && "Null left point");
  assert(right != 0 && "Null right point");
  assert(right->is_right_of(*left) && "Incorrect point order");
}

void Trapezoid::assert_valid(bool tree_complete) const {
#ifndef NDEBUG
  assert(left != 0 && "Null left point");
  assert(right != 0 && "Null right point");

  if (lower_left != 0) {
    assert(lower_left->below == below && lower_left->lower_right == this &&
           "Incorrect lower_left trapezoid");
    assert(get_lower_left_point() == lower_left->get_lower_right_point() &&
           "Incorrect lower left point");
  }

  if (lower_right != 0) {
    assert(lower_right->below == below && lower_right->lower_left == this &&
           "Incorrect lower_right trapezoid");
    assert(get_lower_right_point() == lower_right->get_lower_left_point() &&
           "Incorrect lower right point");
  }

  if (upper_left != 0) {
    assert(upper_left->above == above && upper_left->upper_right == this &&
           "Incorrect upper_left trapezoid");
    assert(get_upper_left_point() == upper_left->get_upper_right_point() &&
           "Incorrect upper left point");
  }

  if (upper_right != 0) {
    assert(upper_right->above == above && upper_right->upper_left == this &&
           "Incorrect upper_right trapezoid");
    assert(get_upper_right_point() == upper_right->get_upper_left_point() &&
           "Incorrect upper right point");
  }

  assert(trapezoid_node != 0 && "Null trapezoid_node");
#endif
}

Point Trapezoid::get_lower_left_point() const {
  double x = left->x;
  return Point(x, below.get_y_at_x(x));
}

Point Trapezoid::get_lower_right_point() const {
  double x = right->x;
  return Point(x, below.get_y_at_x(x));
}

Point Trapezoid::get_upper_left_point() const {
  double x = left->x;
  return Point(x, above.get_y_at_x(x));
}

Point Trapezoid::get_upper_right_point() const {
  double x = right->x;
  return Point(x, above.get_y_at_x(x));
}

void Trapezoid::print_debug() const {
  std::cout << "Trapezoid " << this << " left=" << *left << " right=" << *right
            << " below=" << below << " above=" << above << " ll=" << lower_left
            << " lr=" << lower_right << " ul=" << upper_left
            << " ur=" << upper_right << " node=" << trapezoid_node
            << " llp=" << get_lower_left_point()
            << " lrp=" << get_lower_right_point()
            << " ulp=" << get_upper_left_point()
            << " urp=" << get_upper_right_point() << std::endl;
}

void Trapezoid::set_lower_left(Trapezoid* lower_left_) {
  lower_left = lower_left_;
  if (lower_left != 0) lower_left->lower_right = this;
}

void Trapezoid::set_lower_right(Trapezoid* lower_right_) {
  lower_right = lower_right_;
  if (lower_right != 0) lower_right->lower_left = this;
}

void Trapezoid::set_upper_left(Trapezoid* upper_left_) {
  upper_left = upper_left_;
  if (upper_left != 0) upper_left->upper_right = this;
}

void Trapezoid::set_upper_right(Trapezoid* upper_right_) {
  upper_right = upper_right_;
  if (upper_right != 0) upper_right->upper_left = this;
}

RandomNumberGenerator::RandomNumberGenerator(unsigned long seed)
    : _m(21870), _a(1291), _c(4621), _seed(seed % _m) {}

unsigned long RandomNumberGenerator::operator()(unsigned long max_value) {
  _seed = (_seed * _a + _c) % _m;
  return (_seed * max_value) / _m;
}
