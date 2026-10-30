def find_shortest_path(graph_obj, start_node, end_node):
    """
    Manually implements Dijkstra's Algorithm to find the shortest path.
    Returns: (list_of_airports_in_path, total_distance)
    """
    if start_node not in graph_obj.nodes or end_node not in graph_obj.nodes:
        return [], float('inf')
    unvisited = list(graph_obj.nodes.keys())
    

    distances = {node: float('inf') for node in unvisited}
    distances[start_node] = 0
    
  
    previous_nodes = {node: None for node in unvisited}

    while unvisited:
    
        current_node = unvisited[0]
        for node in unvisited:
            if distances[node] < distances[current_node]:
                current_node = node

       
        if distances[current_node] == float('inf'):
            break
            
       
        if current_node == end_node:
            break

        unvisited.remove(current_node)

        
        for neighbor, weight in graph_obj.get_neighbors(current_node).items():
            if neighbor in unvisited:
               
                new_distance = distances[current_node] + weight
                
        
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node

   
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    
    path.reverse() 
    
    
    if distances[end_node] == float('inf'):
        return [], float('inf')
        
    return path, distances[end_node]