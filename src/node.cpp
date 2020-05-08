#include "node.h"

#include <algorithm>
#include <cassert>
#include <iostream>

#include "trapezoid.h"

Node::Node(const Point* point, Node* left, Node* right) : _type(Type_XNode) {
  assert(point != nullptr && "Invalid point");
  assert(left != nullptr && "Invalid left node");
  assert(right != nullptr && "Invalid right node");
  _union.xnode.point = point;
  _union.xnode.left = left;
  _union.xnode.right = right;
  left->add_parent(this);
  right->add_parent(this);
}

Node::Node(const Edge* edge, Node* below, Node* above) : _type(Type_YNode) {
  assert(edge != nullptr && "Invalid edge");
  assert(below != nullptr && "Invalid below node");
  assert(above != nullptr && "Invalid above node");
  _union.ynode.edge = edge;
  _union.ynode.below = below;
  _union.ynode.above = above;
  below->add_parent(this);
  above->add_parent(this);
}

Node::Node(Trapezoid* trapezoid) : _type(Type_TrapezoidNode) {
  assert(trapezoid != nullptr && "Null Trapezoid");
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
  assert(parent != nullptr && "Null parent");
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
      assert(_union.xnode.left != nullptr && "Null left child");
      assert(_union.xnode.left->has_parent(this) && "Incorrect parent");
      assert(_union.xnode.right != nullptr && "Null right child");
      assert(_union.xnode.right->has_parent(this) && "Incorrect parent");
      _union.xnode.left->assert_valid(tree_complete);
      _union.xnode.right->assert_valid(tree_complete);
      break;
    case Type_YNode:
      assert(_union.ynode.below != nullptr && "Null below child");
      assert(_union.ynode.below->has_parent(this) && "Incorrect parent");
      assert(_union.ynode.above != nullptr && "Null above child");
      assert(_union.ynode.above->has_parent(this) && "Incorrect parent");
      _union.ynode.below->assert_valid(tree_complete);
      _union.ynode.above->assert_valid(tree_complete);
      break;
    case Type_TrapezoidNode:
      assert(_union.trapezoid != nullptr && "Null trapezoid");
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
  assert(child != nullptr && "Null child node");
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
  assert(parent != nullptr && "Null parent");
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
      assert(new_child != nullptr && "Null child node");
      if (_union.xnode.left == old_child)
        _union.xnode.left = new_child;
      else
        _union.xnode.right = new_child;
      break;
    case Type_YNode:
      assert((_union.ynode.below == old_child ||
              _union.ynode.above == old_child) &&
             "Not a child node");
      assert(new_child != nullptr && "Null child node");
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
  assert(new_node != nullptr && "Null replacement node");
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
