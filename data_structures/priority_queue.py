class PQNode:
    """A node storing the passenger/waiting list data and their priority."""
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority 

class PriorityQueue:
    """A Min-Heap implementation for the Waiting List."""
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def insert(self, data, priority):
        new_node = PQNode(data, priority)
        self.heap.append(new_node)
        self._heapify_up(len(self.heap) - 1)

    def pop_for_flight(self, flight_number):
        """Finds, removes, and returns the highest priority passenger for a SPECIFIC flight."""
        if self.is_empty():
            return None
        
        target_index = -1
        best_priority = float('inf')
        
        # Find the highest priority person for this exact flight in the heap array
        for i in range(len(self.heap)):
            if self.heap[i].data['flight_number'] == flight_number:
                if self.heap[i].priority < best_priority:
                    best_priority = self.heap[i].priority
                    target_index = i
                    
        if target_index == -1:
            return None # No one waiting for this flight
            
        result_data = self.heap[target_index].data
        
        # Remove the node and rebalance the Min-Heap
        last_index = len(self.heap) - 1
        if target_index == last_index:
            self.heap.pop() # If it's the last element, just pop it
        else:
            # Swap with the last element, pop, and re-balance
            self.heap[target_index] = self.heap.pop()
            
            # We check if we need to bubble it up or down to keep the heap perfect
            parent = (target_index - 1) // 2
            if target_index > 0 and self.heap[target_index].priority < self.heap[parent].priority:
                self._heapify_up(target_index)
            else:
                self._heapify_down(target_index)
                
        return result_data

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index].priority < self.heap[parent_index].priority:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self.heap[left_child].priority < self.heap[smallest].priority:
            smallest = left_child

        if right_child < len(self.heap) and self.heap[right_child].priority < self.heap[smallest].priority:
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)