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
            if node.parent:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild else None),
                "right": (_to_dict(node.rightchild) if node.rightchild else None),
                "parentkey": pk
            }
        return json.dumps(_to_dict(self.root) if self.root else {}, indent=2)

    def _zig(self, node):
        # Single right rotation
        if node.parent.leftchild == node:
            self._right_rotate(node.parent)
        # Single left rotation
        else:
            self._left_rotate(node.parent)

    def _zig_zig(self, node):
        # Double right rotation
        if node.parent.leftchild == node:
            self._right_rotate(node.parent.parent)
            self._right_rotate(node.parent)
        # Double left rotation
        else:
            self._left_rotate(node.parent.parent)
            self._left_rotate(node.parent)

    def _zig_zag(self, node):
        # Right then left rotation
        if node.parent.leftchild == node:
            self._right_rotate(node.parent)
            self._left_rotate(node.parent)
        # Left then right rotation
        else:
            self._left_rotate(node.parent)
            self._right_rotate(node.parent)

    def _splay(self, node):
        while node.parent:
            if not node.parent.parent:
                self._zig(node)
            elif (node.parent.leftchild == node) == (node.parent.parent.leftchild == node.parent):
                self._zig_zig(node)
            else:
                self._zig_zag(node)

    def _left_rotate(self, x):
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

    def _right_rotate(self, x):
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

    def search(self, key: int) -> Node:
        node = self.root
        while node:
            if key == node.key:
                self._splay(node)
                return node
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild
        return None

    def insert(self, key: int):
        parent = None
        node = self.root
        while node:
            parent = node
            if key < node.key:
                node = node.leftchild
            elif key > node.key:
                node = node.rightchild
            else:  # key == node.key
                self._splay(node)
                return

        new_node = Node(key, parent=parent)
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.leftchild = new_node
        else:
            parent.rightchild = new_node
        self._splay(new_node)

    def delete(self, key: int):
        node = self.search(key)
        if node:
            self._splay(node)  # Splay the node to be deleted to the root
            if not node.leftchild:
                self._transplant(node, node.rightchild)
            elif not node.rightchild:
                self._transplant(node, node.leftchild)
            else:
                y = self._minimum(node.rightchild)
                if y.parent != node:
                    self._transplant(y, y.rightchild)
                    y.rightchild = node.rightchild
                    y.rightchild.parent = y
                self._transplant(node, y)
                y.leftchild = node.leftchild
                y.leftchild.parent = y
            del node

    def _transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.leftchild:
            u.parent.leftchild = v
        else:
            u.parent.rightchild = v
        if v:
            v.parent = u.parent

    def _minimum(self, node):
        while node.leftchild:
            node = node.leftchild
        return node

