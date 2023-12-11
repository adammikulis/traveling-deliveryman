from models import ChainingHashTable
from models import DistanceTable
from models import Package, PackageStatus


class Greedy:
    def __init__(self, distance_data_loader, package_data_loader, truck_manager):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.truck_manager = truck_manager
        self.sorted_packages = self.sort_packages_by_deadline()

    def sort_packages_into_trucks(self):
        for truck in self.truck_manager.trucks:
            # Load packages using Greedy approach on the sorted list
            while len(truck.package_list) < truck.max_packages and self.sorted_packages:
                next_package = self.get_next_valid_closest_package(truck.current_address_id, truck)
                if next_package:
                    self.load_package_into_truck(next_package, truck)
                    if next_package.delivery_group_id != 0:
                        truck.package_groups.append(next_package.delivery_group_id)

    def get_next_valid_closest_package(self, current_address_id, truck):
        closest_distance = float('inf')
        valid_closest_package = None
        for package in self.sorted_packages:
            if package.address_id != current_address_id and package.status != PackageStatus.DELIVERED:
                distance = self.distance_data_loader.distance_table.get_distance(current_address_id, package.address_id)
                eta = truck.calculate_eta(package.address_id)
                if distance < closest_distance and not self.package_arrival_too_soon(package, eta):
                    closest_distance = distance
                    valid_closest_package = package
        return valid_closest_package

    def sort_packages_by_deadline(self):

        # Searching with an index is more flexible than hard-coding 1-40
        package_id_index = self.package_data_loader.package_hash_table.get_package_id_index()
        sorted_packages = [self.package_data_loader.package_hash_table.search(package_id) for package_id in package_id_index]
        # Sort packages by delivery deadline
        sorted_packages.sort(key=lambda package: package.delivery_deadline)
        return sorted_packages

    def load_package_into_truck(self, package, truck):
        if self.can_load_package(truck, package):
            truck.load_package(package.package_id)
            package.status = PackageStatus.IN_TRANSIT
            package.truck_id = truck.truck_id
            print(f"Package {package.package_id} allocated to Truck {truck.truck_id}")
            truck.current_address = package.address_id
            self.sorted_packages.remove(package)  # Remove the package from the sorted list after loading

    def can_load_package(self, truck, package):
        # Check if the truck can load the package
        return (len(truck.package_list) < truck.max_packages and
                (package.required_truck == 0 or package.required_truck == truck.truck_id))

    def package_arrival_too_soon(self, package, eta):
        return eta < package.address_available_time