# This code is adapted from the webinar "How to Dijkstra"
from models import ChainingHashTable

# Used as alternative to dictionary for storing table of paths
class PathInfo:
    def __init__(self, path, distance):
        self.path = path
        self.distance = distance

# This class implements Dijkstra's Shortest Path algorithm with storage for precomputed paths
class DijkstraShortestPath:
    def __init__(self, graph_data_loader):
        self.graph = graph_data_loader.graph
        self.paths = ChainingHashTable(100)
        self.previous_vertex_table = ChainingHashTable(100)
        self.precompute_all_paths()

    def initialize_dijkstra_shortest_path(self, start_vertex_label='0'):
        previous_vertex_table = ChainingHashTable(100)

        for vertex in self.graph.adjacency_list.keys():
            vertex.distance = float('inf')
            previous_vertex_table.insert(vertex, None)

        start_vertex = self.graph.get_vertex(start_vertex_label)
        start_vertex.distance = 0
        unvisited_queue = [vertex for vertex in self.graph.adjacency_list.keys()]

        while unvisited_queue:
            # Find the vertex with the smallest distance in the unvisited queue
            smallest_index = 0
            for i in range(1, len(unvisited_queue)):
                if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                    smallest_index = i

            current_vertex = unvisited_queue.pop(smallest_index)

            # Update distances and previous vertices for adjacent vertices
            for adj_vertex in self.graph.adjacency_list[current_vertex]:
                edge_weight = self.graph.edge_weights.get((current_vertex, adj_vertex), 0.0)
                alternative_path_distance = current_vertex.distance + edge_weight

                if alternative_path_distance < adj_vertex.distance:
                    adj_vertex.distance = alternative_path_distance
                    previous_vertex_table.insert(adj_vertex, current_vertex)  # Update the table

        # Store the computed previous vertex table
        self.previous_vertex_table.insert(start_vertex_label, previous_vertex_table)

    def compute_path_and_distance(self, start_vertex_label, end_vertex_label):
        path = []
        current_vertex = self.graph.get_vertex(end_vertex_label)
        path_distance = 0.0

        # Retrieve the appropriate previous vertex map
        previous_vertex_table = self.previous_vertex_table.search(start_vertex_label)

        while current_vertex is not None and current_vertex.label != start_vertex_label:
            path.append(current_vertex.label)
            prev_vertex = previous_vertex_table.search(current_vertex)

            if prev_vertex is not None:
                edge = (prev_vertex, current_vertex)
                path_distance += self.graph.edge_weights.get(edge, 0.0)
                current_vertex = prev_vertex
            else:
                current_vertex = None

        if current_vertex is None:
            return None, float('inf')  # Indicates no path found

        path.append(start_vertex_label)
        path.reverse()
        return path, path_distance

    # Creates database of paths for quick reference
    def precompute_all_paths(self):
        for start_vertex in self.graph.adjacency_list.keys():
            start_vertex_label = start_vertex.label
            self.initialize_dijkstra_shortest_path(start_vertex_label)

            for end_vertex in self.graph.adjacency_list.keys():
                end_vertex_label = end_vertex.label
                path, distance = self.compute_path_and_distance(start_vertex_label, end_vertex_label)
                path_info = PathInfo(path, distance)
                self.paths.insert((start_vertex_label, end_vertex_label), path_info)

    # Retrieves shortest path from pre-populated database
    def get_shortest_path(self, start_vertex_label, end_vertex_label):
        # Search for the path info in the ChainingHashTable
        path_info = self.paths.search((start_vertex_label, end_vertex_label))

        if path_info:
            # If the path is found in the hash table, return it
            return path_info.path, path_info.distance

        # Fallback if the path is not precomputed
        self.initialize_dijkstra_shortest_path(start_vertex_label)
        path, distance = self.compute_path_and_distance(start_vertex_label, end_vertex_label)

        # Store this new path for future reference in the ChainingHashTable
        path_info = PathInfo(path, distance)
        self.paths.insert((start_vertex_label, end_vertex_label), path_info)
        return path, distance
