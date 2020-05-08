#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iomanip>
#include <limits>
#include <sstream>
#include <stdexcept>

#include "bounding_box.h"
#include "edge.h"
#include "point.h"
#include "trapezoid.h"

namespace py = pybind11;

#define MODULE_NAME _seidel
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define BOUNDING_BOX_NAME "BoundingBox"
#define EDGE_NAME "Edge"
#define POINT_NAME "Point"
#define TRAPEZOID_NAME "Trapezoid"

static std::ostringstream make_stream() {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  return stream;
}

static std::string bool_repr(bool value) { return py::str(py::bool_(value)); }

static std::string point_repr(const Point& self) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << self.x << ", " << self.y
         << ")";
  return stream.str();
}

class EdgeProxy {
 public:
  EdgeProxy(const Point& left_, const Point& right_)
      : left(left_), right(right_), _edge(Edge(&left, &right)){};

  Point left, right;

  const Edge& edge() { return _edge; }

  bool operator==(const EdgeProxy& other) const {
    return left == other.left && right == other.right;
  }

 private:
  Edge _edge;
};

class TrapezoidProxy {
 public:
  TrapezoidProxy(const Point& left_, const Point& right_,
                 const EdgeProxy& above_, const EdgeProxy& below_)
      : left(left_),
        right(right_),
        above(above_),
        below(below_),
        _trapezoid(Trapezoid(&left, &right, below.edge(), above.edge())){};

  Point left;
  Point right;
  EdgeProxy above;
  EdgeProxy below;

 private:
  Trapezoid _trapezoid;
};

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of randomized algorithm for trapezoidal decomposition by R. Seidel.
    )pbdoc";

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<double, double>(), py::arg("x") = 0., py::arg("y") = 0.)
      .def(py::pickle(
          [](const Point& self) {  // __getstate__
            return py::make_tuple(self.x, self.y);
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return Point(tuple[0].cast<double>(), tuple[1].cast<double>());
          }))
      .def(py::self == py::self)
      .def("__repr__", point_repr)
      .def_readwrite("x", &Point::x)
      .def_readwrite("y", &Point::y)
      .def("is_right_of", &Point::is_right_of, py::arg("other"));

  py::class_<BoundingBox>(m, BOUNDING_BOX_NAME)
      .def(py::init<bool, const Point&, const Point&>(),
           py::arg("empty") = true, py::arg("lower") = Point(),
           py::arg("upper") = Point())
      .def(py::pickle(
          [](const BoundingBox& self) {  // __getstate__
            return py::make_tuple(self.empty, self.lower, self.upper);
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return BoundingBox(tuple[0].cast<bool>(), tuple[1].cast<Point>(),
                               tuple[2].cast<Point>());
          }))
      .def("__eq__",
           [](const BoundingBox& self, const BoundingBox& other) {
             return self.empty == other.empty && self.lower == other.lower &&
                    self.upper == other.upper;
           })
      .def("__repr__",
           [](const BoundingBox& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." BOUNDING_BOX_NAME "("
                    << bool_repr(self.empty) << ", " << point_repr(self.lower)
                    << ", " << point_repr(self.upper) << ")";
             return stream.str();
           })
      .def_readwrite("empty", &BoundingBox::empty)
      .def_readwrite("lower", &BoundingBox::lower)
      .def_readwrite("upper", &BoundingBox::upper);

  py::class_<EdgeProxy>(m, EDGE_NAME)
      .def(py::init<const Point&, const Point&>(), py::arg("left"),
           py::arg("right"))
      .def(py::pickle(
          [](const EdgeProxy& self) {  // __getstate__
            return py::make_tuple(self.left, self.right);
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 2) throw std::runtime_error("Invalid state!");
            return EdgeProxy(tuple[0].cast<Point>(), tuple[1].cast<Point>());
          }))
      .def(py::self == py::self)
      .def("__repr__",
           [](const EdgeProxy& self) -> std::string {
             auto stream = make_stream();
             stream << C_STR(MODULE_NAME) "." EDGE_NAME "("
                    << point_repr(self.left) << ", " << point_repr(self.right)
                    << ")";
             return stream.str();
           })
      .def_readwrite("left", &EdgeProxy::left)
      .def_readwrite("right", &EdgeProxy::right);

  py::class_<TrapezoidProxy>(m, TRAPEZOID_NAME)
      .def(py::init<const Point&, const Point&, const EdgeProxy&,
                    const EdgeProxy&>(),
           py::arg("left"), py::arg("right"), py::arg("above"),
           py::arg("below"))
      .def_readwrite("left", &TrapezoidProxy::left)
      .def_readwrite("right", &TrapezoidProxy::right)
      .def_readwrite("above", &TrapezoidProxy::above)
      .def_readwrite("below", &TrapezoidProxy::below);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
