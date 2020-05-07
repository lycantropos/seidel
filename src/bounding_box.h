#ifndef BOUNDING_BOX_H
#define BOUNDING_BOX_H

#include "point.h"

class BoundingBox {
 public:
  BoundingBox(bool empty_ = true, const Point& lower_ = Point(),
              const Point& upper_ = Point());
  void add(const Point& point);
  void expand(const Point& delta);

  // Consider these member variables read-only.
  bool empty;
  Point lower, upper;
};

#endif
