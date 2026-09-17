class Graph:
    """An Adjacency List representation of the Airport network."""
    def __init__(self):
        # Dictionary to store nodes and their connections
        # Example: { 'HYD': {'BLR': 500, 'BOM': 700} }
        self.nodes = {}

    def add_node(self, node):
        """Adds a new airport to the graph."""
        if node not in self.nodes:
            self.nodes[node] = {}

    def add_edge(self, source, destination, distance):
        """Adds a directed route between two airports with a distance (weight)."""
        # Ensure both nodes exist before adding the edge
        self.add_node(source)
        self.add_node(destination)
        
        # Add the distance weight
        self.nodes[source][destination] = distance

    def get_neighbors(self, node):
        """Returns all directly connected airports and their distances."""
        return self.nodes.get(node, {})