from __future__ import annotations

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
        # Removing the minimum node from the roots list
        min_node = self.min_node
        self.roots.remove(min_node)
        
        # Reincorporating the children of the minimum node into the root list
        for child in min_node.children:
            child.flag = False
            child.parent = None
            self.roots.append(child)
            
        # Reorganizing the heap to ensure unique degree
        degrees = self.reorganize_heap()
        
        # Updating the minimum node
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

