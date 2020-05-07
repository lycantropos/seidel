#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iomanip>
#include <limits>
#include <sstream>
#include <stdexcept>

#include "bounding_box.h"
#include "point.h"

namespace py = pybind11;

#define MODULE_NAME _seidel
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define BOUNDING_BOX_NAME "BoundingBox"
#define POINT_NAME "Point"

static std::ostringstream make_stream() {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  return stream;
}

static std::string point_repr(const Point& self) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << self.x << ", " << self.y
         << ")";
  return stream.str();
}

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of randomized algorithm for trapezoidal decomposition by R. Seidel.
    )pbdoc";

  py::class_<BoundingBox>(m, BOUNDING_BOX_NAME)
      .def(py::init<>())
      .def_readwrite("empty", &BoundingBox::empty)
      .def_readwrite("lower", &BoundingBox::lower)
      .def_readwrite("upper", &BoundingBox::upper);

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
      .def_readwrite("y", &Point::y);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
