#include "bounding_box.h"

BoundingBox::BoundingBox(bool empty_, const Point& lower_, const Point& upper_)
    : empty(empty_), lower(lower_), upper(upper_) {}

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
