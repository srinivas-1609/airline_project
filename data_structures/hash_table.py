class HashNode:
    """A node for the linked list used in separate chaining (Collision handling)."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    """A custom Hash Table implementation for user authentication lookups."""
    def __init__(self, capacity=50):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        """Hash function: converts a string key into an integer index."""
        hash_val = 0
        for char in str(key):
            hash_val += ord(char)
        return hash_val % self.capacity

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        index = self._hash(key)
        
        if self.table[index] is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
        
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = HashNode(key, value)
            self.size += 1

    def search(self, key):
        """Searches for a key and returns its value. Returns None if not found."""
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
            
        return None