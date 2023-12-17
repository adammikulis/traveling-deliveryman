import csv
from algorithms import Vertex
# This class loads the csv with distance data and assembles it into a graph
class GraphDataLoader:

    def __init__(self, graph):
        self.graph = graph

    def load_distance_data(self, filename):
        with open(filename) as Distances:
            distance_data = csv.reader(Distances)

            # Read the header row to get the addresses
            header = next(distance_data)

            # Add vertices to the graph
            for address_id in header[1:]:  # Exclude the first column (labels)
                new_vertex = Vertex(str(address_id))
                self.graph.add_vertex(new_vertex)

            # Add edges to the graph
            for distance_row in distance_data:
                from_address = distance_row[0]

                for i, distance in enumerate(distance_row[1:], start=1):
                    if distance:  # Only process filled cells
                        to_address = header[i]
                        distance = float(distance)
                        from_vertex = self.graph.get_vertex(from_address)
                        to_vertex = self.graph.get_vertex(to_address)

                        # Add undirected edge as the distances are symmetric
                        self.graph.add_undirected_edge(from_vertex, to_vertex, distance)