from models import ChainingHashTable
from models import DistanceTable
from models import PackageStatus


class Greedy:

    def __init__(self):
        self.closest_next_package = None

    def get_next_closest_package(self, current_address_id, package_data_loader, distance_data_loader):
        closest_distance = float('inf')
        self.closest_next_package = None

        for package_id in package_data_loader.package_ids:
            package = package_data_loader.package_hash_table.search(package_id)
            if package is not None and package.address_id != current_address_id and package.status != PackageStatus.DELIVERED:
                distance = distance_data_loader.distance_table.get_distance(current_address_id, package.address_id)
                if distance < closest_distance:
                    closest_distance = distance
                    self.closest_next_package = package

        # Update the status of the closest package to DELIVERED
        if self.closest_next_package is not None:
            self.closest_next_package.status = PackageStatus.DELIVERED

        return self.closest_next_package

    # Add that distance to total distance

    # Check if truck is at capacity, if so append the distance back to the hub and move onto next truck on list
    # Load that as the next package in the list for the truck
    # Update the hash table to tell the package what truck it's on
