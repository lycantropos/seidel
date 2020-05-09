#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iomanip>
#include <limits>
#include <sstream>
#include <stdexcept>

#include "bounding_box.h"
#include "edge.h"
#include "node.h"
#include "point.h"
#include "trapezoid.h"

namespace py = pybind11;

#define MODULE_NAME _seidel
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define BOUNDING_BOX_NAME "BoundingBox"
#define EDGE_NAME "Edge"
#define LEAF_NAME "Leaf"
#define POINT_NAME "Point"
#define TRAPEZOID_NAME "Trapezoid"
#define X_NODE_NAME "XNode"

class EdgeProxy {
 public:
  EdgeProxy(const Point& left_, const Point& right_)
      : left(left_), right(right_), _edge(Edge(&left, &right)) {}

  bool operator==(const EdgeProxy& other) const {
    return left == other.left && right == other.right;
  }

  const Edge& edge() const { return _edge; }

  Point left, right;

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
        _trapezoid(std::make_unique<Trapezoid>(&left, &right, below.edge(),
                                               above.edge())) {}

  TrapezoidProxy(const TrapezoidProxy& other)
      : TrapezoidProxy(other.left, other.right, other.above, other.below) {}

  TrapezoidProxy& operator=(const TrapezoidProxy& other) {
    left = other.left;
    right = other.right;
    above = other.above;
    below = other.below;
    _trapezoid =
        std::make_unique<Trapezoid>(&left, &right, below.edge(), above.edge());
    return *this;
  }

  bool operator==(const TrapezoidProxy& other) const {
    return left == other.left && right == other.right && above == other.above &&
           below == other.below;
  }

  Trapezoid* trapezoid() const {
    return new Trapezoid(&left, &right, below.edge(), above.edge());
  }

  Point left;
  Point right;
  EdgeProxy above;
  EdgeProxy below;

 private:
  std::unique_ptr<Trapezoid> _trapezoid;
};

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

static std::string edge_repr(const EdgeProxy& self) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." EDGE_NAME "(" << point_repr(self.left)
         << ", " << point_repr(self.right) << ")";
  return stream.str();
}

static std::string trapezoid_repr(const TrapezoidProxy& self) {
  auto stream = make_stream();
  stream << C_STR(MODULE_NAME) "." TRAPEZOID_NAME "(" << point_repr(self.left)
         << ", " << point_repr(self.right) << ", " << edge_repr(self.above)
         << ", " << edge_repr(self.below) << ")";
  return stream.str();
}

class NodeProxy {
 public:
  virtual Node* node() = 0;
  virtual void print(std::ostream& stream) const = 0;
};

class XNode : public NodeProxy {
 public:
  XNode(const Point& point_, NodeProxy* left_, NodeProxy* right_)
      : point(point_),
        left(left_),
        right(right_),
        _node(&point, left->node(), right->node()) {}

  bool operator==(const XNode& other) const {
    return point == other.point && left == other.left && right == other.right;
  }

  Node* node() override {
    return new Node(&point, left->node(), right->node());
  }

  void print(std::ostream& stream) const override {
    stream << C_STR(MODULE_NAME) "." X_NODE_NAME "(" << point_repr(point)
           << ", ";
    left->print(stream);
    stream << ", ";
    right->print(stream);
    stream << ")";
  }

  Point point;
  NodeProxy* left;
  NodeProxy* right;

 private:
  Node _node;
};

class Leaf : public NodeProxy {
 public:
  Leaf(const TrapezoidProxy& trapezoid_)
      : trapezoid(trapezoid_), _node(trapezoid.trapezoid()) {}

  bool operator==(const Leaf& other) const {
    return trapezoid == other.trapezoid;
  }

  Node* node() override { return new Node(trapezoid.trapezoid()); }

  void print(std::ostream& stream) const override {
    stream << C_STR(MODULE_NAME) "." LEAF_NAME "(" << trapezoid_repr(trapezoid)
           << ")";
  }

  TrapezoidProxy trapezoid;

 private:
  Node _node;
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
      .def("__repr__", edge_repr)
      .def_readonly("left", &EdgeProxy::left)
      .def_readonly("right", &EdgeProxy::right);

  py::class_<TrapezoidProxy>(m, TRAPEZOID_NAME)
      .def(py::init<const Point&, const Point&, const EdgeProxy&,
                    const EdgeProxy&>(),
           py::arg("left"), py::arg("right"), py::arg("above"),
           py::arg("below"))
      .def(py::pickle(
          [](const TrapezoidProxy& self) {  // __getstate__
            return py::make_tuple(self.left, self.right, self.above,
                                  self.below);
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 4) throw std::runtime_error("Invalid state!");
            return std::make_unique<TrapezoidProxy>(
                tuple[0].cast<Point>(), tuple[1].cast<Point>(),
                tuple[2].cast<EdgeProxy>(), tuple[3].cast<EdgeProxy>());
          }))
      .def(py::self == py::self)
      .def("__repr__", trapezoid_repr)
      .def_readonly("left", &TrapezoidProxy::left)
      .def_readonly("right", &TrapezoidProxy::right)
      .def_readonly("above", &TrapezoidProxy::above)
      .def_readonly("below", &TrapezoidProxy::below);

  py::class_<NodeProxy>(m, "Node");

  py::class_<XNode, NodeProxy>(m, X_NODE_NAME)
      .def(py::init<const Point&, NodeProxy*, NodeProxy*>(), py::arg("point"),
           py::arg("left").none(false), py::arg("right").none(false))
      .def(py::self == py::self)
      .def_readonly("point", &XNode::point)
      .def_readonly("left", &XNode::left)
      .def_readonly("right", &XNode::right);

  py::class_<Leaf, NodeProxy>(m, LEAF_NAME)
      .def(py::init<const TrapezoidProxy&>(), py::arg("trapezoid"))
      .def(py::pickle(
          [](const Leaf& self) {  // __getstate__
            return self.trapezoid;
          },
          [](const TrapezoidProxy& trapezoid) {  // __setstate__
            return std::make_unique<Leaf>(trapezoid);
          }))
      .def(py::self == py::self)
      .def("__repr__",
           [](const Leaf& self) {
             auto stream = make_stream();
             self.print(stream);
             return stream.str();
           })
      .def_readonly("trapezoid", &Leaf::trapezoid);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
