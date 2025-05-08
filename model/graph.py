from collections import defaultdict, deque
import heapq

class Graph:
    """
    A graph implementation using adjacency lists (dictionary of dictionaries).
    Supports both directed and undirected weighted graphs.
    """

    def __init__(self):
        """
        Initialize an empty graph using a dictionary of dictionaries representation.
        """
        self.graph = defaultdict(dict)

    def add_node(self, id = 0, node = "unknown", description = "unknown", risk_level = 1):
        """
        Add a node to the graph if it doesn't exist.

        Args:
            node: The node to be added to the graph.
        """
        if node not in self.graph:
            self.graph[node] = {}
    
    def remove_node(self, node):
        """
        Remove a node and all its edges from the graph.

        Args:
            node: The node to be removed.
        """
        if node in self.graph:
            del self.graph[node]
            for n in self.graph:
                if node in self.graph[n]:
                    del self.graph[n][node]
        else:
            raise ValueError(f"Node {node} does not exist in the graph.")

    def add_edge(self, node1, node2, weight=1, directed=False):
        """
        Add an edge between two nodes with an optional weight.

        Args:
            node1: First node of the edge.
            node2: Second node of the edge.
            weight (int, optional): Weight of the edge. Defaults to 1.
            directed (bool, optional): If True, creates a directed edge. Defaults to False.
        """
        self.graph[node1][node2] = weight
        if not directed:
            self.graph[node2][node1] = weight
        

    def dfs_all_paths(self, start, end, path=None, distance=0):
        """
        Perform a Depth-First Search traversal to find all paths from start to end, 
        calculating the total distance of each path.
        
        Args:
            start: Starting node for the traversal.
            end: Ending node for the traversal.
            path: Current path being explored.
            distance: Current accumulated distance.
        
        Returns:
            list: A list of tuples (path, total_distance) for all paths from start to end.
        """
        if path is None:
            path = []
        
        path.append(start)  # Añadir el nodo actual al camino
        
        # Si llegamos al destino, devolvemos el camino y la distancia total
        if start == end:
            return [(list(path), distance)]  # Devolvemos una copia del camino con la distancia
        
        paths = []  # Lista para almacenar los caminos encontrados
        
        # Recorrer los vecinos del nodo actual
        for neighbor, weight in self.graph[start].items():
            if neighbor not in path:  # Evitar ciclos (no visitar un nodo que ya esté en el camino)
                new_paths = self.dfs_all_paths(neighbor, end, path, distance + weight)  # Llamada recursiva
                for new_path, dist in new_paths:
                    paths.append((new_path, dist))  # Guardamos los caminos y su distancia
        
        path.pop()  # Volver atrás en el camino (backtracking)
        return paths

    def dijkstra(self, start):
        """
        Find shortest paths from a start node using Dijkstra's algorithm.

        Args:
            start: Starting node for the algorithm.

        Returns:
            dict: Dictionary with shortest distances to all nodes from start node.
        """
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances