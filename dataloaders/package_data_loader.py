from datetime import time, datetime
from models import Package, ChainingHashTable
import csv


class PackageDataLoader:

    def __init__(self):
        self.package_hash_table = None
        self.total_packages = 0
        self.package_ids = []

    def initialize_hash_table(self, total_packages):
        self.package_hash_table = ChainingHashTable(total_packages)

    def load_package_data(self, filename):
        # Determine the total number of packages
        self.total_packages = self.determine_total_packages(filename)

        # Initialize the hash table with the total number of packages
        self.initialize_hash_table(self.total_packages)

        # Load data from file
        with open(filename) as Packages:
            package_data = csv.reader(Packages, delimiter=",")
            next(package_data)  # skips header
            for package in package_data:
                package_id = int(package[0])
                address_id = int(package[1])
                available_time = datetime.strptime(package[2], "%H:%M").time()
                delivery_deadline = datetime.strptime(package[3], "%H:%M").time()
                weight = float(package[4])
                required_truck = int(package[5])
                delivery_group_id = int(package[6])
                wrong_address = bool(package[7])

                package_object = Package(package_id, address_id, available_time, delivery_deadline, weight,
                                         required_truck, delivery_group_id, wrong_address)
                self.package_hash_table.insert(package_id, package_object)

                self.package_ids.append(package_id)  # Used for referencing later in hash table lookup

    def determine_total_packages(self, filename):
        total_packages = 0
        with open(filename) as Packages:
            package_data = csv.reader(Packages, delimiter=",")
            next(package_data)  # skips header
            for i in package_data:
                total_packages += 1
            return total_packages
