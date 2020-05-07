#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "decomposition.h"

namespace py = pybind11;

#define MODULE_NAME _seidel
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define POINT_NAME "Point"

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of randomized algorithm for trapezoidal decomposition by R. Seidel.
    )pbdoc";

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<double, double>(), py::arg("x") = 0., py::arg("y") = 0.)
      .def(py::self == py::self)
      .def_readwrite("x", &Point::x)
      .def_readwrite("y", &Point::y);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
