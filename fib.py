from __future__ import annotations
from collections import defaultdict

class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False
        self.degree = 0

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val

    def get_degree(self):
        return self.degree

class FibHeap:
    def __init__(self):
        self.roots = []
        self.min_node = None

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        new_node = FibNode(val)
        self.roots.append(new_node)

        # Updating the minimum node if necessary
        if self.min_node is None or val < self.min_node.val:
            self.min_node = new_node
        return new_node
        

    def delete_min(self) -> None:
        if not self.roots:
            return
        # Remove the minimum node from the roots list
        min_node = self.min_node
        self.roots.remove(min_node)
        
        # Reincorporate the children of the minimum node into the root list
        for child in min_node.children:
            child.flag = False
            child.parent = None
            self.roots.append(child)
            
        # Reorganize the heap to ensure at most one root node for each degree
        degrees = self.reorganize_heap()
        
        # Update the minimum node
        self.min_node = min(degrees.values(), key=lambda x: x.val) if degrees else None
        self.roots = list(degrees.values())
    
    def reorganize_heap(self) -> None:
        degrees = {}
        while self.roots:
            curr = self.roots.pop(0)
            degree = len(curr.children)
            if degree not in degrees:
                degrees[degree] = curr
            else:
                exist = degrees[degree]
                if curr.val < exist.val:
                    curr.children.append(exist)
                    exist.parent = curr
                    self.roots.append(curr)
                else:
                    exist.children.append(curr)
                    curr.parent = exist
                    self.roots.append(exist)
                degrees.pop(degree)
        return degrees


    def find_min(self) -> FibNode:
        return self.min_node
        
    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val
        parent = node.parent
        
        # Performing cascading cuts if necessary.
        if parent and node.val < parent.val:
            self.cut_node_from_parent(node, parent)
            self.cascade_cut_node(parent)
        
        # Updating the minimum node
        if node.val < self.min_node.val:
            self.min_node = node

    def consolidate_heap(self):
        # Consolidating the root list to ensure no two trees have the same degree.
        degree_table = [None] * (len(self.roots) * 2)
        new_roots = []

        for root in self.roots:
            x = root
            d = x.get_degree()
            while degree_table[d] is not None:
                y = degree_table[d]
                if x.val > y.val:
                    x, y = y, x
                self.link_child_to_parent(y, x)
                degree_table[d] = None
                d += 1
            degree_table[d] = x

        self.roots = []
        for node in degree_table:
            if node is not None:
                new_roots.append(node)

        self.roots = new_roots

    def cut_node_from_parent(self, child: FibNode, parent: FibNode):
        # Cutting a child node from its parent and add it to the root list.
        if child in parent.children:
            parent.children.remove(child)
            self.roots.append(child)
            child.parent = None
            child.flag = False

        parent.degree -= 1

    def cascade_cut_node(self, node: FibNode):
        # Cascading cuts upward through the tree.
        parent = node.parent
        if parent:
            if not node.flag:
                node.flag = True
            else:
                self.cut_node_from_parent(node, parent)
                self.cascade_cut_node(parent)

    def link_child_to_parent(self, y: FibNode, x: FibNode):
        # Linking a child node to a parent node
        self.roots.remove(y)

        if x.children:
            x.children.append(y)
        else:
            x.children = [y]

        y.parent = x
        y.flag = False
        x.degree += 1
