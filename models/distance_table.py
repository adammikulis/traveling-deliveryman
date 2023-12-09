class DistanceTable:
    def __init__(self, size):
        self.distance_table = [[0 for i in range(size)] for i in range(size)]

    def set_distance(self, address_id_1, address_id_2, distance):
        self.distance_table[address_id_1][address_id_2] = distance
        self.distance_table[address_id_2][address_id_1] = distance

    def get_distance(self, address_id_1, address_id_2):
        return self.distance_table[address_id_1][address_id_2]

    # Used for debugging data loader
    def get_all_distances(self):
        all_distances = []
        for address_id_1, distances in enumerate(self.distance_table):
            for address_id_2, distance in enumerate(distances):
                all_distances.append(f"Distance from {address_id_1} to {address_id_2}: {distance}")
        return all_distances