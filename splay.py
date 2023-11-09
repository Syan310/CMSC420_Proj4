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
        if not self.root:
            self.root = new_node
            return

        node = self._find_node(key)
        if node:
            self._splay(node)
            return  # Node already in the tree, so we splay and exit.

        # Find in-order predecessor if it exists
        predecessor = self._find_max(self.root.leftchild)
        if predecessor:
            self._splay(predecessor)
            predecessor.rightchild = new_node
            new_node.parent = predecessor
            return

        # Find in-order successor if it exists
        successor = self._find_min(self.root.rightchild)
        if successor:
            self._splay(successor)
            successor.leftchild = new_node
            new_node.parent = successor
            return

        # If there's no predecessor or successor, the tree is a single node
        # Insert the new node as the appropriate child of the root.
        if key < self.root.key:
            self.root.leftchild = new_node
        else:
            self.root.rightchild = new_node
        new_node.parent = self.root


    def search(self, key: int):
        node = self._find_node(key)
        if node:
            self._splay(node)
        return node

    def delete(self, key: int):
        node = self._find_node(key)
        if not node:
            return  # Node not found, nothing to delete.

        self._splay(node)
        if not node.leftchild and not node.rightchild:
            # Node is the only node in the tree.
            self.root = None
        elif not node.leftchild or not node.rightchild:
            # Node has only one child.
            self.root = node.leftchild if node.leftchild else node.rightchild
            self.root.parent = None
        else:
            # Node has two children.
            successor = self._find_min(node.rightchild)
            if successor:
                if successor.parent != node:
                    self._transplant(successor, successor.rightchild)
                    successor.rightchild = node.rightchild
                    successor.rightchild.parent = successor
                self._transplant(node, successor)
                successor.leftchild = node.leftchild
                successor.leftchild.parent = successor
            else:
                # If there's no successor, then node is the maximum and has only a left child.
                self.root = node.leftchild
                self.root.parent = None

        del node  # Node is now disconnected from the tree and can be deleted.

    

# This code should be tested thoroughly to ensure its correctness.
