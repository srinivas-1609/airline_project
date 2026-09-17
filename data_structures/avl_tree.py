class AVLNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data  # This will store our actual Flight, Passenger, or Booking info
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, key, data=None):
        # 1. Normal BST Insertion
        if not root:
            return AVLNode(key, data)
        elif key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
        else:
            # Duplicate keys just update the data in our system
            root.data = data
            return root

        # 2. Update height of the ancestor node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Get the balance factor
        balance = self.get_balance(root)

        # 4. If unbalanced, balance it (4 cases)
        # Case 1: Left Left
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        # Case 2: Right Right
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        # Case 3: Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Case 4: Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def get_max_value_node(self, root):
        if root is None or root.right is None:
            return root
        return self.get_max_value_node(root.right)

    def delete(self, root, key):
        # 1. Normal BST Delete
        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Node with two children: Get inorder successor
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.data = temp.data
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        # 2. Update height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Get the balance factor
        balance = self.get_balance(root)

        # 4. If unbalanced, balance it (4 cases)
        # Case 1: Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        # Case 2: Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Case 3: Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        # Case 4: Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, key):
        # Returns the node if found, else None
        if root is None or root.key == key:
            return root
        if root.key < key:
            return self.search(root.right, key)
        return self.search(root.left, key)

    def inorder_traversal(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inorder_traversal(root.left, result)
            result.append((root.key, root.data))
            self.inorder_traversal(root.right, result)
        return result

    def preorder_traversal(self, root, result=None):
        if result is None:
            result = []
        if root:
            result.append((root.key, root.data))
            self.preorder_traversal(root.left, result)
            self.preorder_traversal(root.right, result)
        return result