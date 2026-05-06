class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None
        self.count = 0

    def height(self, n):
        return n.height if n else 0

    def balance(self, n):
        return self.height(n.left) - self.height(n.right)

    def rotate_right(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        return x

    def rotate_left(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        x.height = max(self.height(x.left), self.height(x.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1
        return y

    def insert(self, node, key, value):
        if not node:
            self.count += 1
            return Node(key, value)

        if key < node.key:
            node.left = self.insert(node.left, key, value)
        elif key > node.key:
            node.right = self.insert(node.right, key, value)
        else:
            node.value = value
            return node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        b = self.balance(node)

        if b > 1 and key < node.left.key:
            return self.rotate_right(node)
        if b < -1 and key > node.right.key:
            return self.rotate_left(node)
        if b > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if b < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.value
        return self.search(node.left, key) if key < node.key else self.search(node.right, key)

    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.key, ":", node.value)
            self.inorder(node.right)

# teste
tree = AVL()
tree.root = tree.insert(tree.root, "casa", "moradia")
tree.root = tree.insert(tree.root, "bola", "esfera")
tree.root = tree.insert(tree.root, "abacaxi", "fruta")

print("Busca:", tree.search(tree.root, "bola"))
tree.inorder(tree.root)
print("Total:", tree.count)