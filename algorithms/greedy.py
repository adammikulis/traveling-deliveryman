from models import ChainingHashTable
from models import DistanceTable
from models import PackageStatus


class Greedy:
    def __init__(self, distance_data_loader, package_data_loader):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader

    def get_next_closest_package(self, current_address_id):
        closest_distance = float('inf')
        closest_next_package = None
        for package_id in self.package_data_loader.package_ids:
            package = self.package_data_loader.package_hash_table.search(package_id)
            if package and package.address_id != current_address_id and package.status != PackageStatus.DELIVERED:
                distance = self.distance_data_loader.distance_table.get_distance(current_address_id, package.address_id)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_next_package = package
        return closest_next_package

    def sort_packages_into_trucks(self, truck_manager):
        sorted_packages = self._sort_packages_by_priority()
        for package in sorted_packages:
            self._allocate_package_to_truck(package, truck_manager)

    def _sort_packages_by_priority(self):
        package_id_index = self.package_data_loader.package_hash_table.get_package_id_index()
        all_packages = [self.package_data_loader.package_hash_table.search(package_id) for package_id in package_id_index]
        # Sort packages by your chosen criteria
        return sorted(all_packages, key=lambda package: package.delivery_deadline)

    def _allocate_package_to_truck(self, package, truck_manager):
        for truck in truck_manager.trucks:
            if self._can_load_package(truck, package):
                truck.load_package(package.package_id)
                package.status = PackageStatus.IN_TRANSIT  # Update package status
                package.truck_id = truck.truck_id
                return True
        return False  # If no truck can accommodate the package

    def _can_load_package(self, truck, package):
        # Check if the truck can load the package
        return (len(truck.package_list) < truck.max_packages and
                (package.required_truck == 0 or package.required_truck == truck.truck_id))
