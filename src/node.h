#ifndef NODE_H
#define NODE_H

#include <list>
#include <set>

#include "edge.h"
#include "point.h"

struct Trapezoid;  // Forward declaration.

/* Node of the trapezoid map search tree.  There are 3 possible types:
 * Type_XNode, Type_YNode and Type_TrapezoidNode.  Data members are
 * represented using a union: an XNode has a Point and 2 child nodes
 * (left and right of the point), a YNode has an Edge and 2 child nodes
 * (below and above the edge), and a TrapezoidNode has a Trapezoid.
 * Each Node has multiple parents so it can appear in the search tree
 * multiple times without having to create duplicate identical Nodes.
 * The parent collection acts as a reference count to the number of times
 * a Node occurs in the search tree.  When the parent count is reduced to
 * zero a Node can be safely deleted. */
class Node {
 public:
  Node(const Point* point, Node* left, Node* right);  // Type_XNode.
  Node(const Edge* edge, Node* below, Node* above);   // Type_YNode.
  Node(Trapezoid* trapezoid);                         // Type_TrapezoidNode.

  ~Node();

  void add_parent(Node* parent);

  /* Recurse through the search tree and assert that everything is valid.
   * Reduces to a no-op if NDEBUG is defined. */
  void assert_valid(bool tree_complete) const;

  bool has_child(const Node* child) const;
  bool has_no_parents() const;
  bool has_parent(const Node* parent) const;

  /* Remove a parent from this Node.  Return true if no parents remain
   * so that this Node can be deleted. */
  bool remove_parent(Node* parent);

  void replace_child(Node* old_child, Node* new_child);

  // Replace this node with the specified new_node in all parents.
  void replace_with(Node* new_node);

  /* Recursive search through the tree to find the Node containing the
   * specified Point point. */
  const Node* search(const Point& xy);

  /* Recursive search through the tree to find the Trapezoid containing
   * the left endpoint of the specified Edge.  Return 0 if fails, which
   * can only happen if the triangulation is invalid. */
  Trapezoid* search(const Edge& edge);

  Node(const Node& other) = delete;
  Node& operator=(const Node& other) = delete;

  typedef enum { Type_XNode, Type_YNode, Type_TrapezoidNode } Type;
  Type type;

  union {
    struct {
      const Point* point;  // Not owned.
      Node* left;          // Owned.
      Node* right;         // Owned.
    } xnode;
    struct {
      const Edge* edge;  // Not owned.
      Node* below;       // Owned.
      Node* above;       // Owned.
    } ynode;
    Trapezoid* trapezoid;  // Owned.
  } data;

  typedef std::list<Node*> Parents;
  Parents parents;  // Not owned.
};

#endif
