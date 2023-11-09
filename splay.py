from __future__ import annotations
import json
from typing import List

verbose = False

class Node:
    def __init__(self, key: int, leftchild=None, rightchild=None, parent=None):
        self.key = key
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.parent = parent

class SplayTree:
    def __init__(self, root: Node = None):
        self.root = root

    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr, indent=2)

    # Helper method to perform a right rotation
    def _right_rotate(self, x):
        y = x.leftchild
        x.leftchild = y.rightchild
        if y.rightchild is not None:
            y.rightchild.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.rightchild:
            x.parent.rightchild = y
        else:
            x.parent.leftchild = y
        y.rightchild = x
        x.parent = y

    # Helper method to perform a left rotation
    def _left_rotate(self, x):
        y = x.rightchild
        x.rightchild = y.leftchild
        if y.leftchild is not None:
            y.leftchild.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.leftchild:
            x.parent.leftchild = y
        else:
            x.parent.rightchild = y
        y.leftchild = x
        x.parent = y

    # Splaying operation
    def _splay(self, node):
        while node.parent is not None:  # Node is not the root
            if node.parent.parent is None:  # Zig
                if node.parent.leftchild == node:
                    self._right_rotate(node.parent)
                else:
                    self._left_rotate(node.parent)
            elif node.parent.leftchild == node and node.parent.parent.leftchild == node.parent:  # Zig-Zig
                self._right_rotate(node.parent.parent)
                self._right_rotate(node.parent)
            elif node.parent.rightchild == node and node.parent.parent.rightchild == node.parent:  # Zig-Zig
                self._left_rotate(node.parent.parent)
                self._left_rotate(node.parent)
            elif node.parent.leftchild == node and node.parent.parent.rightchild == node.parent:  # Zig-Zag
                self._right_rotate(node.parent)
                self._left_rotate(node.parent)
            elif node.parent.rightchild == node and node.parent.parent.leftchild == node.parent:  # Zig-Zag
                self._left_rotate(node.parent)
                self._right_rotate(node.parent)

    # Search operation
    def search(self, key: int):
        node = self.root
        while node is not None:
            if key == node.key:
                self._splay(node)
                return node
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild
        return None

    # Insert operation
    def insert(self, key: int):
        if self.root is None:
            self.root = Node(key)
            return
        node = self.root
        while True:
            if key < node.key:
                if node.leftchild is None:
                    node.leftchild = Node(key, parent=node)
                    self._splay(node.leftchild)
                    break
                node = node.leftchild
            elif key > node.key:
                if node.rightchild is None:
                    node.rightchild = Node(key, parent=node)
                    self._splay(node.rightchild)
                    break
                node = node.rightchild
            else:
                self._splay(node)
                break  # Duplicate keys are not allowed

    # Delete operation
    def delete(self, key: int):
        node = self.search(key)
        if node is None:
            return  # Node with key doesn't exist

        self._splay(node)  # Splay the node to be deleted to the root

        if node.leftchild is not None:
            left_subtree = node.leftchild
            left_subtree.parent = None
        else:
            left_subtree = None

        if node.rightchild is not None:
            right_subtree = node.rightchild
            right_subtree.parent = None
        else:
            right_subtree = None

        if left_subtree is not None:
            max_node = left_subtree
            while max_node.rightchild is not None:
                max_node = max_node.rightchild
            self._splay(max_node)
            max_node.rightchild = right_subtree
            if right_subtree is not None:
                right_subtree.parent = max_node
            self.root = max_node
        else:
            self.root = right_subtree

