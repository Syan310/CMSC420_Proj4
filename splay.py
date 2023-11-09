from __future__ import annotations
import json
from typing import Optional

class Node:
    def __init__(self, key: int, leftchild: Optional[Node] = None, rightchild: Optional[Node] = None, parent: Optional[Node] = None):
        self.key = key
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.parent = parent

class SplayTree:
    def __init__(self, root: Optional[Node] = None):
        self.root = root

    def dump(self) -> str:
            def _to_dict(node: Optional[Node]) -> dict:
                if not node:
                    return None
                pk = node.parent.key if node.parent else None
                return {
                    "key": node.key,
                    "left": _to_dict(node.leftchild),
                    "right": _to_dict(node.rightchild),
                    "parentkey": pk
                }
            return json.dumps(_to_dict(self.root), indent=2)
        
    def _splay(self, node: Optional[Node]):
        while node.parent:
            if not node.parent.parent:
                if node.parent.leftchild == node:
                    self._right_rotate(node.parent)
                else:
                    self._left_rotate(node.parent)
            elif node.parent.leftchild == node and node.parent.parent.leftchild == node.parent:
                self._right_rotate(node.parent.parent)
                self._right_rotate(node.parent)
            elif node.parent.rightchild == node and node.parent.parent.rightchild == node.parent:
                self._left_rotate(node.parent.parent)
                self._left_rotate(node.parent)
            elif node.parent.leftchild == node and node.parent.parent.rightchild == node.parent:
                self._right_rotate(node.parent)
                self._left_rotate(node.parent)
            else:
                self._left_rotate(node.parent)
                self._right_rotate(node.parent)

    def _left_rotate(self, x: Node):
        y = x.rightchild
        x.rightchild = y.leftchild
        if y.leftchild:
            y.leftchild.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.leftchild:
            x.parent.leftchild = y
        else:
            x.parent.rightchild = y
        y.leftchild = x
        x.parent = y

    def _right_rotate(self, x: Node):
        y = x.leftchild
        x.leftchild = y.rightchild
        if y.rightchild:
            y.rightchild.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.rightchild:
            x.parent.rightchild = y
        else:
            x.parent.leftchild = y
        y.rightchild = x
        x.parent = y

    def _find_node(self, key: int) -> Optional[Node]:
        node = self.root
        while node:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild
        return None

    def _find_min(self, node: Optional[Node]) -> Optional[Node]:
        while node and node.leftchild:
            node = node.leftchild
        return node

    def _find_max(self, node: Optional[Node]) -> Optional[Node]:
        while node and node.rightchild:
            node = node.rightchild
        return node

    def insert(self, key: int):
        new_node = Node(key)
        # If the tree is empty, insert the new node as the root.
        if not self.root:
            self.root = new_node
            return

        # Step 1: Find the node if it already exists.
        node = self._find_node(key)
        if node:
            # The node is already in the tree, splay it to the root.
            self._splay(node)
        else:
            # Step 2: The node is not in the tree; we need to find the in-order predecessor or successor.
            node = self.root
            while True:
                if key < node.key:
                    if node.leftchild:
                        node = node.leftchild
                    else:
                        # The in-order predecessor is the rightmost node of the left subtree.
                        # If the left subtree does not exist, then the current node is the in-order successor.
                        break
                else:
                    if node.rightchild:
                        node = node.rightchild
                    else:
                        # The in-order successor is the leftmost node of the right subtree.
                        # If the right subtree does not exist, then the current node is the in-order predecessor.
                        break
            
            # Step 3: Splay the in-order predecessor or successor.
            self._splay(node)

            # Step 4: Insert the new node and adjust the tree.
            if key < node.key:
                new_node.rightchild = node
                new_node.leftchild = node.leftchild
                if node.leftchild:
                    node.leftchild.parent = new_node
                node.leftchild = None
            else:
                new_node.leftchild = node
                new_node.rightchild = node.rightchild
                if node.rightchild:
                    node.rightchild.parent = new_node
                node.rightchild = None
            node.parent = new_node
            self.root = new_node



    def search(self, key: int) -> Optional[Node]:
        node = self.root
        last_visited = None
        while node:
            last_visited = node
            if key == node.key:
                self._splay(node)
                return node
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild

        if last_visited:
            self._splay(last_visited)

        return None  # Return None to indicate the search failed, but the last visited node was splayed.


    def _transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.leftchild:
            u.parent.leftchild = v
        else:
            u.parent.rightchild = v
        if v:
            v.parent = u.parent
            
    def delete(self, key: int):
        node_to_delete = self.search(key)  # This will splay the node if it exists
        if node_to_delete:
            if node_to_delete.leftchild and node_to_delete.rightchild:
                successor = self._find_min(node_to_delete.rightchild)
                if successor.parent != node_to_delete:
                    self._transplant(successor, successor.rightchild)
                    successor.rightchild = node_to_delete.rightchild
                    if node_to_delete.rightchild:  # Check if the node to delete has a right child
                        node_to_delete.rightchild.parent = successor
                successor.leftchild = node_to_delete.leftchild
                if node_to_delete.leftchild:  # Check if the node to delete has a left child
                    node_to_delete.leftchild.parent = successor
                self._transplant(node_to_delete, successor)
            elif node_to_delete.leftchild:
                self._transplant(node_to_delete, node_to_delete.leftchild)
            elif node_to_delete.rightchild:
                self._transplant(node_to_delete, node_to_delete.rightchild)
            else:
                self.root = None  # The deleted node was the last node in the tree

            # Set the new root's parent to None
            if self.root:
                self.root.parent = None
            del node_to_delete



