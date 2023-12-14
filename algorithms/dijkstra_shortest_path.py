class DijkstraShortestPath:
    def __init__(self, graph):
        self.graph = graph
        self.paths = {}  # Dictionary to store precomputed paths
        self.previous_vertex_maps = {}  # New dictionary to store previous vertex maps
        self.precompute_all_paths()

    def initialize_dijkstra_shortest_path(self, start_vertex_label='0'):
        # Initialize a new previous vertex map for this start vertex
        previous_vertex_map = {}
        for vertex in self.graph.adjacency_list.keys():
            vertex.distance = float('inf')
            previous_vertex_map[vertex] = None

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
                    previous_vertex_map[adj_vertex] = current_vertex

        # Store the computed previous vertex map
        self.previous_vertex_maps[start_vertex_label] = previous_vertex_map

    def compute_path_and_distance(self, start_vertex_label, end_vertex_label):
        path = []
        current_vertex = self.graph.get_vertex(end_vertex_label)
        path_distance = 0.0

        # Retrieve the appropriate previous vertex map
        previous_vertex_map = self.previous_vertex_maps[start_vertex_label]

        while current_vertex is not None and current_vertex.label != start_vertex_label:
            path.append(current_vertex.label)
            prev_vertex = previous_vertex_map[current_vertex]

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

    def precompute_all_paths(self):
        for start_vertex in self.graph.adjacency_list.keys():
            start_vertex_label = start_vertex.label
            self.initialize_dijkstra_shortest_path(start_vertex_label)

            for end_vertex in self.graph.adjacency_list.keys():
                end_vertex_label = end_vertex.label
                path, distance = self.compute_path_and_distance(start_vertex_label, end_vertex_label)
                self.paths[(start_vertex_label, end_vertex_label)] = {'path': path, 'distance': distance}

    def get_shortest_path(self, start_vertex_label, end_vertex_label):
        if (start_vertex_label, end_vertex_label) in self.paths:
            path_info = self.paths[(start_vertex_label, end_vertex_label)]
            return path_info['path'], path_info['distance']

        # Fallback to computation if the path is not precomputed
        self.initialize_dijkstra_shortest_path(start_vertex_label)
        start_vertex = self.graph.get_vertex(start_vertex_label)
        end_vertex = self.graph.get_vertex(end_vertex_label)
        path, distance = self.compute_path_and_distance(start_vertex, end_vertex)

        # Store this path for future reference
        self.paths[(start_vertex_label, end_vertex_label)] = {'path': path, 'distance': distance}
        return path, distance

    def get_direct_distance(self, start_vertex_label, end_vertex_label):
        edge_key = (start_vertex_label, end_vertex_label)
        return self.graph.edge_weights.get(edge_key, None)