# Below is the initial implementation for the SplayTree class with the required methods and rotations.
# Note: The detailed implementation of rotations and splay operations will be done iteratively.

class Node:
    def __init__(self, key: int, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return f"Node({self.key})"

class SplayTree:
    def __init__(self, root=None):
        self.root = root

    def _zig(self, x):
        # Right rotation
        p = x.parent
        if p:
            gp = p.parent
            if gp:
                if gp.left == p:
                    gp.left = x
                else:
                    gp.right = x
            x.parent = gp
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
            p.parent = x
            if x.parent is None:
                self.root = x

    def _zag(self, x):
        # Left rotation
        p = x.parent
        if p:
            gp = p.parent
            if gp:
                if gp.left == p:
                    gp.left = x
                else:
                    gp.right = x
            x.parent = gp
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
            p.parent = x
            if x.parent is None:
                self.root = x

    def _splay(self, x):
        while x.parent:
            p = x.parent
            gp = p.parent
            if gp is None:
                # Zig step
                if p.left == x:
                    self._zig(x)
                else:
                    self._zag(x)
            elif gp.left == p and p.left == x:
                # Zig-zig step
                self._zig(p)
                self._zig(x)
            elif gp.right == p and p.right == x:
                # Zag-zag step
                self._zag(p)
                self._zag(x)
            elif gp.left == p and p.right == x:
                # Zig-zag step
                self._zag(x)
                self._zig(x)
            else:
                # Zag-zig step
                self._zig(x)
                self._zag(x)

    def _find(self, key):
        # Binary search tree find operation
        node = self.root
        last = self.root
        next_node = None
        while node:
            last = node
            if key < node.key:
                next_node = node.left
            elif key > node.key:
                next_node = node.right
            else:
                next_node = None
                break
            node = next_node
        return last

    def search(self, key: int):
        node = self._find(key)
        self._splay(node)
        return node.key == key if node else False

    def insert(self, key: int):
        parent = self._find(key)
        node = Node(key)
        if parent is None:
            self.root = node
        else:
            node.parent = parent
            if key < parent.key:
                parent.left = node
            else:
                parent.right = node
        self._splay(node)

    def delete(self, key: int):
        if self.search(key):
            node = self.root
            if node.left:
                left_subtree = SplayTree(node.left)
                left_subtree._splay(max(node.left.key))
                left_subtree.root.right = node.right
                if node.right:
                    node.right.parent = left_subtree.root
                self.root = left_subtree.root
            else:
                self.root = node.right
                if node.right:
                    node.right.parent = None
            node.left = node.right = node.parent = None

