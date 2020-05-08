#ifndef NODE_H
#define NODE_H

#include <list>
#include <set>

#include "edge.h"
#include "point.h"

class Node;  // Forward declaration.

// Helper structure used by TrapezoidalMap::get_tree_stats.
struct NodeStats {
  NodeStats()
      : node_count(0),
        trapezoid_count(0),
        max_parent_count(0),
        max_depth(0),
        sum_trapezoid_depth(0.0) {}

  long node_count, trapezoid_count, max_parent_count, max_depth;
  double sum_trapezoid_depth;
  std::set<const Node*> unique_nodes, unique_trapezoid_nodes;
};

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

  // Recurse through the tree to return statistics about it.
  void get_stats(int depth, NodeStats& stats) const;

  bool has_child(const Node* child) const;
  bool has_no_parents() const;
  bool has_parent(const Node* parent) const;

  /* Recurse through the tree and print a textual representation to
   * stdout.  Argument depth used to indent for readability. */
  void print(int depth = 0) const;

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

  /* Copy constructor and assignment operator defined but not implemented
   * to prevent objects being copied. */
  Node(const Node& other);
  Node& operator=(const Node& other);

 private:
  typedef enum { Type_XNode, Type_YNode, Type_TrapezoidNode } Type;
  Type _type;

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
  } _union;

  typedef std::list<Node*> Parents;
  Parents _parents;  // Not owned.
};

#endif
