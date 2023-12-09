from models import DistanceTable
import csv


class DistanceDataLoader:

    def __init__(self):
        self.distance_table = None

    def initialize_distance_table(self, total_addresses):
        self.distance_table = DistanceTable(total_addresses)

    def load_distance_data(self, filename):
        with open(filename) as Distances:
            distance_data = csv.reader(Distances)
            header = next(distance_data)  # Store header row for reference

            # Initialize the distance table with the total number of addresses
            total_addresses = len(header) - 1
            self.initialize_distance_table(total_addresses)

            for distance_row in distance_data:
                from_address_id = int(distance_row[0])

                for i, distance in enumerate(distance_row[1:], start=1):
                    if distance:  # Only process filled cells
                        to_address_id = int(header[i])
                        dist = float(distance)
                        self.distance_table.set_distance(from_address_id, to_address_id, dist)
