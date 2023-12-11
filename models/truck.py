from datetime import time
from dataloaders import DistanceDataLoader, PackageDataLoader


class Truck:

    def __init__(self, distance_data_loader, package_data_loader, truck_id, max_packages=16, average_speed=18, miles_driven=0, assigned_driver_id=None):
        self.truck_id = truck_id
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.max_packages = max_packages
        self.average_speed = average_speed
        self.miles_driven = miles_driven
        self.package_list = []
        self.assigned_driver_id = 0
        self.earliest_leave_time = time(0, 0)
        self.can_leave_hub = False

    def load_package(self, package_id):
        self.package_list.append(package_id)

    def unload_package(self, package_id):
        self.package_list.remove(package_id)

    def drive_to(self, distance):
        self.miles_driven += distance

    def can_load_package(self, package):
        return len(self.package_list) < self.max_packages and package.required_truck in [0, self.truck_id]

    def sort_package_list(self):
        self.package_list.sort(key=lambda package: ())

    def set_earliest_leave_time(self):
        for package_id in self.package_list:
            package = self.package_data_loader.package_hash_table.search(package_id)
            if package and package.available_time > self.earliest_leave_time:
                self.earliest_leave_time = package.available_time

    def set_can_leave_hub(self, current_time):
        if self.earliest_leave_time >= current_time:
            self.can_leave_hub = True


    def __repr__(self):
        return f"Truck ID: {self.truck_id} Current Packages: {self.package_list}"