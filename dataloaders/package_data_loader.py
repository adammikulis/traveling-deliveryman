from datetime import time, datetime
from models import Package, PackageHashTable

import csv


class PackageDataLoader:

    def __init__(self):
        self.package_hash_table = None
        self.total_packages = 0
        self.package_groups = {} # Special packages
        self.package_required_trucks = {} # Special packages
        self.package_id_list = []  # Used for status printing

    def initialize_hash_table(self, total_packages):
        self.package_hash_table = PackageHashTable(total_packages)

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
                self.package_id_list.append(package_id)
                address_id = int(package[1])
                available_time = datetime.strptime(package[2], "%H:%M").time()
                delivery_deadline = datetime.strptime(package[3], "%H:%M").time()
                weight = float(package[4])
                required_truck = int(package[5])
                delivery_group_id = int(package[6])
                wrong_address = bool(package[7])
                address_available_time = datetime.strptime(package[8], "%H:%M").time()

                package_object = Package(package_id, address_id, available_time, delivery_deadline, weight,
                                         required_truck, delivery_group_id, wrong_address, address_available_time)

                self.package_hash_table.insert(package_id, package_object)


                # Store any package groups to reference for sorting
                group_id = package_object.delivery_group_id
                if group_id != 0:
                    if group_id not in self.package_groups:
                        self.package_groups[group_id] = []
                    self.package_groups[group_id].append(package_id)

                # Store any required trucks to reference for sorting
                truck_id = package_object.required_truck
                if truck_id != 0:
                    if truck_id not in self.package_required_trucks:
                        self.package_required_trucks[truck_id] = []
                    self.package_required_trucks[truck_id].append(package_id)

    # Used for table sizing
    def determine_total_packages(self, filename):
        total_packages = 0
        with open(filename) as Packages:
            package_data = csv.reader(Packages, delimiter=",")
            next(package_data)  # skips header
            for i in package_data:
                total_packages += 1
            return total_packages

    def print_all_package_status(self):
        for package_id in self.package_id_list:
            print(self.package_hash_table.search(package_id))

    def return_all_package_info(self, package_id):
        package = self.package_hash_table.search(package_id)
        return package.address_id, package.truck_id, package.status, package.delivered_at, package.delivered_on_time