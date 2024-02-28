# explanations for member functions are provided in requirements.py
from __future__ import annotations

class FibNodeLazy:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNodeLazy):
        return self.val == other.val

class FibHeapLazy:
    def __init__(self):
        self.roots = []

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNodeLazy:
        new_node = FibNodeLazy(val)
        self.roots.append(new_node)
        return new_node
        
    def delete_min_lazy(self) -> None:
        if not self.roots:
            return

        min_node = min(self.roots, key=lambda x: x.val)
        self.roots.remove(min_node)

        if min_node.children:
            for child in min_node.children:
                self.roots.append(child)
                child.parent = None

        # Mark the minimum node as vacant
        min_node.flag = True
        min_node.parent = None
        min_node.children = []

    def find_min_lazy(self) -> FibNodeLazy:
        if not self.roots:
            return None
        return min(self.roots, key=lambda x: x.val)

    def decrease_priority(self, node: FibNodeLazy, new_val: int) -> None:
        node.val = new_val
        parent = node.parent
        
        # Performing cascading cuts if necessary.
        if parent and node.val < parent.val:
            self.cut_node_from_parent(node, parent)
            self.cutting_sequence_upward(parent)
        
        # Updating the minimum node
        if node.val < self.min_node.val:
            self.min_node = node

    def cut_node_from_parent(self, child: FibNode, parent: FibNode):
        # Cutting a child node from its parent and add it to the root list.
        if child in parent.children:
            parent.children.remove(child)
            self.roots.append(child)
            child.parent = None
            child.flag = False

        parent.degree -= 1

    def cutting_sequence_upward(self, node: FibNode):
        # Cascading cuts upward through the tree.
        parent = node.parent
        if parent:
            if not node.flag:
                node.flag = True
            else:
                self.cut_node_from_parent(node, parent)
                self.cutting_sequence_upward(parent)

# class FibHeapLazy:
#     def __init__(self):
#         # you may define any additional member variables you need
#         self.roots = []
#         pass

#     def get_roots(self) -> list:
#         return self.roots

#     def insert(self, val: int) -> FibNodeLazy:
#         pass
        
#     def delete_min_lazy(self) -> None:
#         pass

#     def find_min_lazy(self) -> FibNodeLazy:
#         pass

#     def decrease_priority(self, node: FibNodeLazy, new_val: int) -> None:
#         pass

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
