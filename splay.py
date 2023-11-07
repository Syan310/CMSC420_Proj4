from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
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
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    # Search
    # Helper function: left rotation

    def _right_rotate(self, node):
        left = node.leftchild
        node.leftchild = left.rightchild
        if left.rightchild:
            left.rightchild.parent = node
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.rightchild:
            node.parent.rightchild = left
        else:
            node.parent.leftchild = left
        left.rightchild = node
        node.parent = left

    def _left_rotate(self, node):
        right = node.rightchild
        node.rightchild = right.leftchild
        if right.leftchild:
            right.leftchild.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.leftchild:
            node.parent.leftchild = right
        else:
            node.parent.rightchild = right
        right.leftchild = node
        node.parent = right

    def _splay(self, node):
        while node.parent:  # Continue until the node becomes the root
            if node.parent.parent is None:  # Zig step
                if node == node.parent.leftchild:
                    self._right_rotate(node.parent)
                else:
                    self._left_rotate(node.parent)
            else:
                p = node.parent
                gp = p.parent
                if node == p.leftchild:
                    if p == gp.leftchild:  # Zig-Zig step (Left-Left)
                        self._right_rotate(gp)
                        self._right_rotate(p)
                    else:  # Zig-Zag step (Left-Right)
                        self._right_rotate(p)
                        self._left_rotate(gp)
                else:
                    if p == gp.rightchild:  # Zig-Zig step (Right-Right)
                        self._left_rotate(gp)
                        self._left_rotate(p)
                    else:  # Zig-Zag step (Right-Left)
                        self._left_rotate(p)
                        self._right_rotate(gp)
                        
        # Ensure the node is set as root after splaying
        self.root = node


    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return

        node = self.root
        while node:
            if key < node.key:
                if not node.leftchild:
                    node.leftchild = Node(key, parent=node)
                    self._splay(node.leftchild)
                    break
                node = node.leftchild
            else:
                if not node.rightchild:
                    node.rightchild = Node(key, parent=node)
                    self._splay(node.rightchild)
                    break
                node = node.rightchild

    def _find_node(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild
        return None
    
    def _transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.leftchild:
            u.parent.leftchild = v
        else:
            u.parent.rightchild = v
        if v:
            v.parent = u.parent

    def delete(self, key):
        node_to_remove = self._find_node(key)
        if node_to_remove:
            self._splay(node_to_remove)
            if not node_to_remove.leftchild:
                self._transplant(node_to_remove, node_to_remove.rightchild)
            elif not node_to_remove.rightchild:
                self._transplant(node_to_remove, node_to_remove.leftchild)
            else:
                # Find the smallest node in the right subtree
                min_node = node_to_remove.rightchild
                while min_node.leftchild:
                    min_node = min_node.leftchild
                if min_node.parent != node_to_remove:
                    self._transplant(min_node, min_node.rightchild)
                    min_node.rightchild = node_to_remove.rightchild
                    min_node.rightchild.parent = min_node
                self._transplant(node_to_remove, min_node)
                min_node.leftchild = node_to_remove.leftchild
                min_node.leftchild.parent = min_node

    def search(self, key):
        node = self.root
        last = None
        while node:
            last = node
            if key == node.key:
                self._splay(node)
                return
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild
        if last:
            self._splay(last)
