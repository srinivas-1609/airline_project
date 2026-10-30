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

      
        y.right = z
        z.left = T3

       
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

       
        y.left = z
        z.right = T2

        
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, key, data=None):
      
        if not root:
            return AVLNode(key, data)
        elif key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
        else:
           
            root.data = data
            return root

        
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
       
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
         
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.data = temp.data
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root
        
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
     
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, key):
       
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