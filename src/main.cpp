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
#include "trapezoidal_map.h"

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
#define Y_NODE_NAME "YNode"

static std::string bool_repr(bool value) { return py::str(py::bool_(value)); }

static std::ostream& operator<<(std::ostream& stream, const Point& point) {
  return stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << point.x << ", "
                << point.y << ")";
}

static std::ostream& operator<<(std::ostream& stream, const BoundingBox& box) {
  return stream << C_STR(MODULE_NAME) "." BOUNDING_BOX_NAME "("
                << bool_repr(box.empty) << ", " << box.lower << ", "
                << box.upper << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Edge& edge) {
  return stream << C_STR(MODULE_NAME) "." EDGE_NAME "(" << *edge.left << ", "
                << *edge.right << ")";
}

static std::ostream& operator<<(std::ostream& stream,
                                const Trapezoid& trapezoid) {
  return stream << C_STR(MODULE_NAME) "." TRAPEZOID_NAME "(" << *trapezoid.left
                << ", " << *trapezoid.right << ", " << trapezoid.above << ", "
                << trapezoid.below << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Node& node) {
  switch (node.type) {
    case Node::Type_XNode:
      return stream << C_STR(MODULE_NAME) "." X_NODE_NAME "("
                    << *node.data.xnode.point << ", " << *node.data.xnode.left
                    << ", " << *node.data.xnode.right << ")";
    case Node::Type_YNode:
      return stream << C_STR(MODULE_NAME) "." Y_NODE_NAME "("
                    << *node.data.ynode.edge << ", " << *node.data.ynode.above
                    << ", " << *node.data.ynode.below << ")";
    case Node::Type_TrapezoidNode:
      return stream << C_STR(MODULE_NAME) "." LEAF_NAME "("
                    << *node.data.trapezoid << ")";
  }
}

template <class Object>
std::string repr(const Object& object) {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  stream << object;
  return stream.str();
}

static bool are_edges_equal(const Edge& first, const Edge& second) {
  return ((*first.left) == (*second.left)) &&
         ((*first.right) == (*second.right));
}

static bool are_trapezoids_equal(const Trapezoid& first,
                                 const Trapezoid& second) {
  return ((*first.left) == (*second.left)) &&
         ((*first.right) == (*second.right)) &&
         are_edges_equal(first.above, second.above) &&
         are_edges_equal(first.below, second.below);
}

static bool are_nodes_equal(const Node& first, const Node& second) {
  if (first.type != second.type) return false;
  switch (first.type) {
    case Node::Type_XNode: {
      return ((*first.data.xnode.point) == (*second.data.xnode.point)) &&
             are_nodes_equal(*first.data.xnode.left, *second.data.xnode.left) &&
             are_nodes_equal(*first.data.xnode.right, *second.data.xnode.right);
    }
    case Node::Type_YNode: {
      return are_edges_equal(*first.data.ynode.edge, *second.data.ynode.edge) &&
             are_nodes_equal(*first.data.ynode.above,
                             *second.data.ynode.above) &&
             are_nodes_equal(*first.data.ynode.below, *second.data.ynode.below);
    }
    case Node::Type_TrapezoidNode: {
      return are_trapezoids_equal(*first.data.trapezoid,
                                  *second.data.trapezoid);
    }
  }
}

class EdgeProxy {
 public:
  EdgeProxy(const Point& left_, const Point& right_)
      : left(left_), right(right_), _edge(Edge(&left, &right)) {}

  EdgeProxy(const EdgeProxy& edge) : EdgeProxy(edge.left, edge.right) {}

  EdgeProxy(const Edge& edge) : EdgeProxy(*edge.left, *edge.right) {}

  EdgeProxy& operator=(const EdgeProxy& edge) {
    left = edge.left;
    right = edge.right;
    _edge = Edge(&left, &right);
    return *this;
  }

  bool operator==(const EdgeProxy& other) const {
    return are_edges_equal(_edge, other._edge);
  }

  const Edge& edge() const { return _edge; }

  Point left, right;

 private:
  Edge _edge;
};

static std::ostream& operator<<(std::ostream& stream, const EdgeProxy& edge) {
  return stream << edge.edge();
}

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

  TrapezoidProxy(const Trapezoid& trapezoid)
      : TrapezoidProxy(*trapezoid.left, *trapezoid.right,
                       EdgeProxy(trapezoid.above), EdgeProxy(trapezoid.below)) {
  }

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
    return are_trapezoids_equal(*_trapezoid, *other._trapezoid);
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

static std::ostream& operator<<(std::ostream& stream,
                                const TrapezoidProxy& trapezoid) {
  return stream << *trapezoid.trapezoid();
}

class NodeProxy {
 public:
  virtual ~NodeProxy() {}
  virtual Node* node_copy() const = 0;
  virtual Node& node() = 0;
  virtual const Node& node() const = 0;

  bool operator==(const NodeProxy& other) const {
    return are_nodes_equal(node(), other.node());
  }
};

static std::ostream& operator<<(std::ostream& stream, const NodeProxy& node) {
  return stream << node.node();
}

class XNode : public NodeProxy {
 public:
  XNode(const Point& point_, std::shared_ptr<NodeProxy> left_,
        std::shared_ptr<NodeProxy> right_)
      : point(point_),
        left(left_),
        right(right_),
        _node(&point, left->node_copy(), right->node_copy()) {}

  Node* node_copy() const override {
    return new Node(&point, left->node_copy(), right->node_copy());
  }

  const Node& node() const override { return _node; }

  Node& node() override { return _node; }

  Point point;
  std::shared_ptr<NodeProxy> left;
  std::shared_ptr<NodeProxy> right;

 private:
  Node _node;
};

class YNode : public NodeProxy {
 public:
  YNode(const EdgeProxy& edge_, std::shared_ptr<NodeProxy> above_,
        std::shared_ptr<NodeProxy> below_)
      : edge(edge_),
        above(above_),
        below(below_),
        _node(&edge.edge(), below->node_copy(), above->node_copy()) {}

  Node* node_copy() const override {
    return new Node(&edge.edge(), below->node_copy(), above->node_copy());
  }

  const Node& node() const override { return _node; }

  Node& node() override { return _node; }

  EdgeProxy edge;
  std::shared_ptr<NodeProxy> above;
  std::shared_ptr<NodeProxy> below;

 private:
  Node _node;
};

class Leaf : public NodeProxy {
 public:
  Leaf(const TrapezoidProxy& trapezoid_)
      : trapezoid(trapezoid_), _node(trapezoid.trapezoid()) {}

  Node* node_copy() const override { return new Node(trapezoid.trapezoid()); }

  const Node& node() const override { return _node; }

  Node& node() override { return _node; }

  TrapezoidProxy trapezoid;

 private:
  Node _node;
};

static std::shared_ptr<NodeProxy> node_to_proxy(const Node& node) {
  switch (node.type) {
    case Node::Type_XNode:
      return std::make_shared<XNode>(*node.data.xnode.point,
                                     node_to_proxy(*node.data.xnode.left),
                                     node_to_proxy(*node.data.xnode.right));
    case Node::Type_YNode:
      return std::make_shared<YNode>(*node.data.ynode.edge,
                                     node_to_proxy(*node.data.ynode.above),
                                     node_to_proxy(*node.data.ynode.below));
    case Node::Type_TrapezoidNode:
      return std::make_shared<Leaf>(*node.data.trapezoid);
  }
}

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(
        Python binding of randomized algorithm for trapezoidal decomposition by R. Seidel.
    )pbdoc";

  m.def("build_graph", [](const std::vector<Point>& points) {
    TrapezoidalMap map{points};
    map.build();
    return node_to_proxy(map.tree());
  });

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
      .def(py::self + py::self)
      .def(py::self - py::self)
      .def(py::self * float())
      .def("__repr__", repr<Point>)
      .def_readwrite("x", &Point::x)
      .def_readwrite("y", &Point::y)
      .def("cross_z", &Point::cross_z, py::arg("other"))
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
      .def("__repr__", repr<BoundingBox>)
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
      .def("__repr__", repr<EdgeProxy>)
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
      .def("__repr__", repr<TrapezoidProxy>)
      .def_readonly("left", &TrapezoidProxy::left)
      .def_readonly("right", &TrapezoidProxy::right)
      .def_readonly("above", &TrapezoidProxy::above)
      .def_readonly("below", &TrapezoidProxy::below);

  py::class_<NodeProxy, std::shared_ptr<NodeProxy>>(m, "Node");

  py::class_<XNode, NodeProxy, std::shared_ptr<XNode>>(m, X_NODE_NAME)
      .def(py::init<const Point&, std::shared_ptr<NodeProxy>,
                    std::shared_ptr<NodeProxy>>(),
           py::arg("point"), py::arg("left").none(false),
           py::arg("right").none(false))
      .def(py::pickle(
          [](const XNode& self) {  // __getstate__
            return py::make_tuple(self.point, self.left, self.right);
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return std::make_unique<XNode>(
                tuple[0].cast<const Point&>(),
                tuple[1].cast<std::shared_ptr<NodeProxy>>(),
                tuple[2].cast<std::shared_ptr<NodeProxy>>());
          }))
      .def(py::self == py::self)
      .def("__repr__", repr<XNode>)
      .def_readonly("point", &XNode::point)
      .def_readonly("left", &XNode::left)
      .def_readonly("right", &XNode::right);

  py::class_<YNode, NodeProxy, std::shared_ptr<YNode>>(m, Y_NODE_NAME)
      .def(py::init<const EdgeProxy&, std::shared_ptr<NodeProxy>,
                    std::shared_ptr<NodeProxy>>(),
           py::arg("edge"), py::arg("above").none(false),
           py::arg("below").none(false))
      .def(py::pickle(
          [](const YNode& self) {  // __getstate__
            return py::make_tuple(self.edge, self.above, self.below);
          },
          [](py::tuple tuple) {  // __setstate__
            if (tuple.size() != 3) throw std::runtime_error("Invalid state!");
            return std::make_unique<YNode>(
                tuple[0].cast<const EdgeProxy&>(),
                tuple[1].cast<std::shared_ptr<NodeProxy>>(),
                tuple[2].cast<std::shared_ptr<NodeProxy>>());
          }))
      .def(py::self == py::self)
      .def("__repr__", repr<YNode>)
      .def_readonly("edge", &YNode::edge)
      .def_readonly("above", &YNode::above)
      .def_readonly("below", &YNode::below);

  py::class_<Leaf, NodeProxy, std::shared_ptr<Leaf>>(m, LEAF_NAME)
      .def(py::init<const TrapezoidProxy&>(), py::arg("trapezoid"))
      .def(py::pickle(
          [](const Leaf& self) {  // __getstate__
            return self.trapezoid;
          },
          [](const TrapezoidProxy& trapezoid) {  // __setstate__
            return std::make_unique<Leaf>(trapezoid);
          }))
      .def(py::self == py::self)
      .def("__repr__", repr<Leaf>)
      .def_readonly("trapezoid", &Leaf::trapezoid);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
