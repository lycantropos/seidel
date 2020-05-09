#ifndef POINT_H
#define POINT_H

struct Point {
  Point(double x_ = 0., double y_ = 0.);
  double cross_z(const Point& other) const;    // z-component of cross product.
  bool is_right_of(const Point& other) const;  // Compares x then y.
  bool operator==(const Point& other) const;
  bool operator!=(const Point& other) const;
  Point operator*(const double& multiplier) const;
  const Point& operator+=(const Point& other);
  const Point& operator-=(const Point& other);
  Point operator+(const Point& other) const;
  Point operator-(const Point& other) const;

  double x, y;
};

#endif
