#include "point.h"

Point::Point(double x_, double y_) : x(x_), y(y_) {}

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
