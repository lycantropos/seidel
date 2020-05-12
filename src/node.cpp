#include "node.h"

#include <algorithm>
#include <cassert>

#include "trapezoid.h"

Node::Node(const Point* point, Node* left, Node* right) : type(Type_XNode) {
  assert(point != nullptr && "Invalid point");
  assert(left != nullptr && "Invalid left node");
  assert(right != nullptr && "Invalid right node");
  data.xnode.point = point;
  data.xnode.left = left;
  data.xnode.right = right;
  left->add_parent(this);
  right->add_parent(this);
}

Node::Node(const Edge* edge, Node* below, Node* above) : type(Type_YNode) {
  assert(edge != nullptr && "Invalid edge");
  assert(below != nullptr && "Invalid below node");
  assert(above != nullptr && "Invalid above node");
  data.ynode.edge = edge;
  data.ynode.below = below;
  data.ynode.above = above;
  below->add_parent(this);
  above->add_parent(this);
}

Node::Node(Trapezoid* trapezoid) : type(Type_TrapezoidNode) {
  assert(trapezoid != nullptr && "Null Trapezoid");
  data.trapezoid = trapezoid;
  trapezoid->trapezoid_node = this;
}

Node::~Node() {
  switch (type) {
    case Type_XNode:
      if (data.xnode.left->remove_parent(this)) delete data.xnode.left;
      if (data.xnode.right->remove_parent(this)) delete data.xnode.right;
      break;
    case Type_YNode:
      if (data.ynode.below->remove_parent(this)) delete data.ynode.below;
      if (data.ynode.above->remove_parent(this)) delete data.ynode.above;
      break;
    case Type_TrapezoidNode:
      delete data.trapezoid;
      break;
  }
}

void Node::add_parent(Node* parent) {
  assert(parent != nullptr && "Null parent");
  assert(parent != this && "Cannot be parent of self");
  assert(!has_parent(parent) && "Parent already in collection");
  parents.push_back(parent);
}

void Node::assert_valid(bool tree_complete) const {
#ifndef NDEBUG
  // Check parents.
  for (Parents::const_iterator it = parents.begin(); it != parents.end();
       ++it) {
    Node* parent = *it;
    assert(parent != this && "Cannot be parent of self");
    assert(parent->has_child(this) && "Parent missing child");
  }

  // Check children, and recurse.
  switch (type) {
    case Type_XNode:
      assert(data.xnode.left != nullptr && "Null left child");
      assert(data.xnode.left->has_parent(this) && "Incorrect parent");
      assert(data.xnode.right != nullptr && "Null right child");
      assert(data.xnode.right->has_parent(this) && "Incorrect parent");
      data.xnode.left->assert_valid(tree_complete);
      data.xnode.right->assert_valid(tree_complete);
      break;
    case Type_YNode:
      assert(data.ynode.below != nullptr && "Null below child");
      assert(data.ynode.below->has_parent(this) && "Incorrect parent");
      assert(data.ynode.above != nullptr && "Null above child");
      assert(data.ynode.above->has_parent(this) && "Incorrect parent");
      data.ynode.below->assert_valid(tree_complete);
      data.ynode.above->assert_valid(tree_complete);
      break;
    case Type_TrapezoidNode:
      assert(data.trapezoid != nullptr && "Null trapezoid");
      assert(data.trapezoid->trapezoid_node == this &&
             "Incorrect trapezoid node");
      data.trapezoid->assert_valid(tree_complete);
      break;
  }
#endif
}

bool Node::has_child(const Node* child) const {
  assert(child != nullptr && "Null child node");
  switch (type) {
    case Type_XNode:
      return (data.xnode.left == child || data.xnode.right == child);
    case Type_YNode:
      return (data.ynode.below == child || data.ynode.above == child);
    default:  // Type_TrapezoidNode:
      return false;
  }
}

bool Node::has_no_parents() const { return parents.empty(); }

bool Node::has_parent(const Node* parent) const {
  return (std::find(parents.begin(), parents.end(), parent) != parents.end());
}

bool Node::remove_parent(Node* parent) {
  assert(parent != nullptr && "Null parent");
  assert(parent != this && "Cannot be parent of self");
  Parents::iterator it = std::find(parents.begin(), parents.end(), parent);
  assert(it != parents.end() && "Parent not in collection");
  parents.erase(it);
  return parents.empty();
}

void Node::replace_child(Node* old_child, Node* new_child) {
  switch (type) {
    case Type_XNode:
      assert((data.xnode.left == old_child || data.xnode.right == old_child) &&
             "Not a child Node");
      assert(new_child != nullptr && "Null child node");
      if (data.xnode.left == old_child)
        data.xnode.left = new_child;
      else
        data.xnode.right = new_child;
      break;
    case Type_YNode:
      assert((data.ynode.below == old_child || data.ynode.above == old_child) &&
             "Not a child node");
      assert(new_child != nullptr && "Null child node");
      if (data.ynode.below == old_child)
        data.ynode.below = new_child;
      else
        data.ynode.above = new_child;
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
  // child replaced it is removed from the parents collection.
  while (!parents.empty()) parents.front()->replace_child(this, new_node);
}

const Node* Node::search(const Point& xy) const {
  switch (type) {
    case Type_XNode:
      if (xy == *data.xnode.point)
        return this;
      else if (xy.is_right_of(*data.xnode.point))
        return data.xnode.right->search(xy);
      else
        return data.xnode.left->search(xy);
    case Type_YNode: {
      int orient = data.ynode.edge->get_point_orientation(xy);
      if (orient == 0)
        return this;
      else if (orient < 0)
        return data.ynode.above->search(xy);
      else
        return data.ynode.below->search(xy);
    }
    default:  // Type_TrapezoidNode:
      return this;
  }
}

Trapezoid* Node::search(const Edge& edge) {
  switch (type) {
    case Type_XNode:
      if (edge.left == data.xnode.point)
        return data.xnode.right->search(edge);
      else {
        if (edge.left->is_right_of(*data.xnode.point))
          return data.xnode.right->search(edge);
        else
          return data.xnode.left->search(edge);
      }
    case Type_YNode:
      if (edge.left == data.ynode.edge->left) {
        // Coinciding left edge points.
        if (edge.get_slope() == data.ynode.edge->get_slope()) {
          assert(0 && "Invalid triangulation, common left points");
          return 0;
        }
        if (edge.get_slope() > data.ynode.edge->get_slope())
          return data.ynode.above->search(edge);
        else
          return data.ynode.below->search(edge);
      } else if (edge.right == data.ynode.edge->right) {
        // Coinciding right edge points.
        if (edge.get_slope() == data.ynode.edge->get_slope()) {
          assert(0 && "Invalid triangulation, common right points");
          return 0;
        }
        if (edge.get_slope() > data.ynode.edge->get_slope())
          return data.ynode.below->search(edge);
        else
          return data.ynode.above->search(edge);
      } else {
        int orient = data.ynode.edge->get_point_orientation(*edge.left);
        if (orient == 0) {
          assert(0 && "Invalid triangulation, point on edge");
          return 0;
        }
        if (orient < 0)
          return data.ynode.above->search(edge);
        else
          return data.ynode.below->search(edge);
      }
    default:  // Type_TrapezoidNode:
      return data.trapezoid;
  }
}
