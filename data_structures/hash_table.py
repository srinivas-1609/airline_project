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
        # Add up the ASCII values of each character in the string
        for char in str(key):
            hash_val += ord(char)
        # Modulo division ensures the index fits within our table capacity
        return hash_val % self.capacity

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        index = self._hash(key)
        
        # If the slot is empty, place the new node there
        if self.table[index] is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
        else:
            # COLLISION HANDLING: Separate Chaining
            # Traverse the linked list at this index
            current = self.table[index]
            while current:
                # If key already exists, update its value
                if current.key == key:
                    current.value = value
                    return
                # If we reach the end of the chain, stop
                if current.next is None:
                    break
                current = current.next
            
            # Add the new node at the end of the chain
            current.next = HashNode(key, value)
            self.size += 1

    def search(self, key):
        """Searches for a key and returns its value. Returns None if not found."""
        index = self._hash(key)
        current = self.table[index]
        
        # Traverse the chain to find the exact key
        while current:
            if current.key == key:
                return current.value
            current = current.next
            
        return None