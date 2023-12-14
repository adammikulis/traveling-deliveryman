class Graph:
    def __init__(self):
        self.adjacency_list = {}  # vertex dictionary
        self.edge_weights = {}  # edge dictionary

    def add_vertex(self, new_vertex):
        if new_vertex not in self.adjacency_list:
            self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def get_vertex(self, label):
        for vertex in self.adjacency_list.keys():
            if vertex.label == label:
                return vertex
        return None