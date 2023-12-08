from models.chaining_hash_table import ChainingHashTable


class Truck:

    def __init__(self, truck_number=0, max_packages=16, average_speed=18):
        self.truck_number = truck_number
        self.max_packages = max_packages
        self.average_speed = average_speed
        self.package_list = ChainingHashTable(max_packages)
