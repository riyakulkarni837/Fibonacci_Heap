# explanations for member functions are provided in requirements.py

# 12041645
# Shreya Chetan Pawaskar
# pawaskas@uci.edu

from __future__ import annotations

class FibNode:
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

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    def __init__(self):
        # Initialize a Fibonacci Heap with roots and the minimum node
        self.roots = []
        self.min = None

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        new_node = FibNode(val)
        # Update the minimum node if needed
        if self.min is None or self.min.val > val:
            self.min = new_node
        # Add the new node to the roots list
        self.roots.append(new_node)
        return new_node

    def update_min(self):
        for node in self.roots:
            if self.min is None or self.min.val > node.val:
                self.min = node

    def delete_min(self) -> None:
        if not self.roots:
            return

        min_node = self.min
        # Remove the minimum node from the roots list
        self.roots.remove(min_node)
        # Add the children of the minimum node back to the roots list
        for child in min_node.children:
            child.flag = False
            child.parent = None
            self.roots.append(child)

        # Reorganize the heap to ensure at most one root node for each degree
        degrees = {}
        while len(self.roots) != 0:
            current_node = self.roots.pop(0)
            degree = len(current_node.children)
            if degree not in degrees:
                degrees[degree] = current_node
            else:
                existing_node = degrees[degree]
                if current_node.val < existing_node.val:
                    current_node.children.append(existing_node)
                    existing_node.parent = current_node 
                    self.roots.append(current_node)
                else:
                    existing_node.children.append(current_node)
                    current_node.parent = existing_node
                    self.roots.append(existing_node)
                degrees.pop(degree)

        for node in degrees.values():
            self.roots.append(node)
        self.min = None
        self.update_min()

    def find_min(self) -> FibNode:
        return self.min

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val
        # Perform a cut operation to promote the node to the root list
        self.promote(node)
        # Update the minimum node
        self.update_min()
        
    def promote(self, node: FibNode) -> None:
        # Cut a node and promote it to the root list
        if node not in self.roots:
            parent = node.parent
            parent.children.remove(node)
            node.flag = False
            # Add the cut node to the roots list
            self.roots.append(node)
            # Recursively cut the parent if needed
            if parent.flag:
                self.promote(parent)
            elif parent not in self.roots:
                parent.flag = True