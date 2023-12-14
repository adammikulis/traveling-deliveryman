class DijkstraShortestPath:
    def __init__(self, g, start_vertex):
        self.unvisited_queue = []
        self.g = g
        self.start_vertex = start_vertex

    def dijkstra_shortest_path(self):
        for vertex in self.g.adjacency_list.keys():
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
            for adj_vertex in self.g.adjacency_list[current_vertex]:
                edge_weight = self.g.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight

                if alternative_path_distance < adj_vertex.distance:
                    adj_vertex.distance = alternative_path_distance
                    adj_vertex.prev_vertex = current_vertex

    def get_shortest_path(self, start_vertex, end_vertex):
        path = []
        current_vertex = end_vertex

        while current_vertex is not None and current_vertex != start_vertex:
            path.append(current_vertex.label)
            current_vertex = current_vertex.prev_vertex

        if current_vertex is None:
            raise Exception("No path found")

        path.append(start_vertex.label)
        path.reverse()
        return path