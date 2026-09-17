def find_shortest_path(graph_obj, start_node, end_node):
    """
    Manually implements Dijkstra's Algorithm to find the shortest path.
    Returns: (list_of_airports_in_path, total_distance)
    """
    if start_node not in graph_obj.nodes or end_node not in graph_obj.nodes:
        return [], float('inf')

    # List of unvisited airports
    unvisited = list(graph_obj.nodes.keys())
    
    # Track the shortest distance to each airport (start at infinity)
    distances = {node: float('inf') for node in unvisited}
    distances[start_node] = 0
    
    # Track the previous airport to reconstruct the final route
    previous_nodes = {node: None for node in unvisited}

    while unvisited:
        # 1. Find the unvisited airport with the lowest distance
        current_node = unvisited[0]
        for node in unvisited:
            if distances[node] < distances[current_node]:
                current_node = node

        # If the smallest distance is infinity, the remaining nodes are unreachable
        if distances[current_node] == float('inf'):
            break
            
        # If we reached our destination, we can stop searching
        if current_node == end_node:
            break

        unvisited.remove(current_node)

        # 2. Check all neighbors of the current airport
        for neighbor, weight in graph_obj.get_neighbors(current_node).items():
            if neighbor in unvisited:
                # Calculate new possible distance
                new_distance = distances[current_node] + weight
                
                # If it's shorter than the previously known distance, update it
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node

    # 3. Reconstruct the path backwards from destination to start
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    
    path.reverse() # Flip it so it goes from Start -> End
    
    # If the destination is unreachable
    if distances[end_node] == float('inf'):
        return [], float('inf')
        
    return path, distances[end_node]