class DijkstraShortestPath:
    def __init__(self, graph):
        self.unvisited_queue = []
        self.graph = graph
        self.start_vertex = self.graph.get_vertex('0')

    def dijkstra_shortest_path(self):
        for vertex in self.graph.adjacency_list.keys():
            self.unvisited_queue.append(vertex)

        self.start_vertex.distance = 0

        while len(self.unvisited_queue) > 0:
            # Find the vertex with the smallest distance in the unvisited queue
            smallest_index = 0
            for i in range(1, len(self.unvisited_queue)):
                if self.unvisited_queue[i].distance < self.unvisited_queue[smallest_index].distance:
                    smallest_index = i

            current_vertex = self.unvisited_queue.pop(smallest_index)

            # Update distances for adjacent vertices
            for adj_vertex in self.graph.adjacency_list[current_vertex]:
                edge_weight = self.graph.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight

                if alternative_path_distance < adj_vertex.distance:
                    adj_vertex.distance = alternative_path_distance
                    adj_vertex.previous_vertex = current_vertex

    def get_shortest_path(self, start_vertex_label, end_vertex_label):
        path = []
        start_vertex = self.graph.get_vertex(start_vertex_label)
        end_vertex = self.graph.get_vertex(end_vertex_label)
        current_vertex = end_vertex

        while current_vertex is not None and current_vertex != start_vertex:
            path.append(current_vertex.label)
            current_vertex = current_vertex.previous_vertex

        if current_vertex is None:
            raise Exception("No path found")

        path.append(start_vertex.label)
        path.reverse()
        return path

    def get_direct_distance(self, address_label_1, address_label_2):
        # Retrieve vertices corresponding to the addresses
        vertex1 = self.graph.get_vertex(address_label_1)
        vertex2 = self.graph.get_vertex(address_label_2)

        if vertex1 and vertex2:
            # Return the direct distance from the edge weights
            return self.graph.edge_weights.get((vertex1, vertex2), None)
        else:
            return None