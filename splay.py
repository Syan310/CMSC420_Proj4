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
        
    def splay(self, node: Optional[Node]):
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

    def rotate_left(self, node: Node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.up = node
        right_child.up = node.up
        if not node.up:
            self.top = right_child
        elif node is node.up.left:
            node.up.left = right_child
        else:
            node.up.right = right_child
        right_child.left = node
        node.up = right_child

    def rotate_right(self, node: Node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.up = node
        left_child.up = node.up
        if not node.up:
            self.top = left_child
        elif node is node.up.right:
            node.up.right = left_child
        else:
            node.up.left = left_child
        left_child.right = node
        node.up = left_child


    def search(self, key: int) -> Optional[Node]:
        node = self.root
        last_visited = None
        while node:
            last_visited = node
            if key == node.key:
                self.splay(node)
                return node
            elif key < node.key:
                node = node.leftchild
            else:
                node = node.rightchild

        if last_visited:
            self.splay(last_visited)

        return None  
    
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

    def _find_max(self, node: Optional[Node]) -> Optional[Node]:
        while node and node.rightchild:
            node = node.rightchild
        return node    
   
    def _find_min(self, node: Optional[Node]) -> Optional[Node]:
        while node and node.leftchild:
            node = node.leftchild
        return node




    def insert(self, key: int):
        new_node = Node(key)
      
        if not self.root:
            self.root = new_node
            return

      
        node = self._find_node(key)
        if node:
           
            self.splay(node)
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
            
           
            self.splay(node)

            
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
        to_delete = self.search(key)  
        if to_delete:
            if to_delete.leftchild and to_delete.rightchild:
                successor = self._find_min(to_delete.rightchild)
                if successor.parent != to_delete:
                    self._splay(successor)
                    self._transplant(to_delete, successor)
                    successor.leftchild = to_delete.leftchild
                    to_delete.leftchild.parent = successor
                else:
                    self._transplant(to_delete, successor)
                    successor.leftchild = to_delete.leftchild
                    if to_delete.leftchild:
                        to_delete.leftchild.parent = successor
            elif to_delete.leftchild:
                self._transplant(to_delete, to_delete.leftchild)
            elif to_delete.rightchild:
                self._transplant(to_delete, to_delete.rightchild)
            else:
                self.root = None  
            
            if self.root:
                self.root.parent = None
            del to_delete


