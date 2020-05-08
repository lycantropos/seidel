#include "trapezoid.h"

#include <cassert>
#include <iostream>

#include "node.h"

Trapezoid::Trapezoid(const Point* left_, const Point* right_,
                     const Edge& below_, const Edge& above_)
    : left(left_),
      right(right_),
      below(below_),
      above(above_),
      lower_left(nullptr),
      lower_right(nullptr),
      upper_left(nullptr),
      upper_right(nullptr),
      trapezoid_node(nullptr) {
  assert(left != nullptr && "Null left point");
  assert(right != nullptr && "Null right point");
  assert(right->is_right_of(*left) && "Incorrect point order");
}

void Trapezoid::assert_valid(bool tree_complete) const {
#ifndef NDEBUG
  assert(left != nullptr && "Null left point");
  assert(right != nullptr && "Null right point");

  if (lower_left != nullptr) {
    assert(lower_left->below == below && lower_left->lower_right == this &&
           "Incorrect lower_left trapezoid");
    assert(get_lower_left_point() == lower_left->get_lower_right_point() &&
           "Incorrect lower left point");
  }

  if (lower_right != nullptr) {
    assert(lower_right->below == below && lower_right->lower_left == this &&
           "Incorrect lower_right trapezoid");
    assert(get_lower_right_point() == lower_right->get_lower_left_point() &&
           "Incorrect lower right point");
  }

  if (upper_left != nullptr) {
    assert(upper_left->above == above && upper_left->upper_right == this &&
           "Incorrect upper_left trapezoid");
    assert(get_upper_left_point() == upper_left->get_upper_right_point() &&
           "Incorrect upper left point");
  }

  if (upper_right != nullptr) {
    assert(upper_right->above == above && upper_right->upper_left == this &&
           "Incorrect upper_right trapezoid");
    assert(get_upper_right_point() == upper_right->get_upper_left_point() &&
           "Incorrect upper right point");
  }

  assert(trapezoid_node != nullptr && "Null trapezoid_node");
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
  if (lower_left != nullptr) lower_left->lower_right = this;
}

void Trapezoid::set_lower_right(Trapezoid* lower_right_) {
  lower_right = lower_right_;
  if (lower_right != nullptr) lower_right->lower_left = this;
}

void Trapezoid::set_upper_left(Trapezoid* upper_left_) {
  upper_left = upper_left_;
  if (upper_left != nullptr) upper_left->upper_right = this;
}

void Trapezoid::set_upper_right(Trapezoid* upper_right_) {
  upper_right = upper_right_;
  if (upper_right != nullptr) upper_right->upper_left = this;
}
