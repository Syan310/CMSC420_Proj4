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

    def min(self, node: Optional[Node]) -> Optional[Node]:
        while node and node.leftchild:
            node = node.leftchild
        return node


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

        return None  


    def insert(self, key: int):
        new_node = Node(key)
        if not self.root:
            self.root = new_node
            return
        
        node = self._find_node(key)
        if node:
            self._splay(node)
        else:
            node = self.root
            while True:
                if key < node.key:
                    if node.leftchild:
                        node = node.leftchild
                    else:
                        break
                else:
                    if node.rightchild:
                        node = node.rightchild
                    else:
                        break
            
          
            self._splay(node)

           
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
        node_to_delete = self.search(key)  
        if node_to_delete:
            if node_to_delete.leftchild and node_to_delete.rightchild:
               
                successor = self.min(node_to_delete.rightchild)
                if successor.parent != node_to_delete:
                    self._splay(successor)
                    self._transplant(node_to_delete, successor)
                    successor.leftchild = node_to_delete.leftchild
                    node_to_delete.leftchild.parent = successor
                else:
                    self._transplant(node_to_delete, successor)
                    successor.leftchild = node_to_delete.leftchild
                    if node_to_delete.leftchild:
                        node_to_delete.leftchild.parent = successor
            elif node_to_delete.leftchild:
                self._transplant(node_to_delete, node_to_delete.leftchild)
            elif node_to_delete.rightchild:
                self._transplant(node_to_delete, node_to_delete.rightchild)
            else:
                self.root = None  
            if self.root:
                self.root.parent = None
            del node_to_delete


