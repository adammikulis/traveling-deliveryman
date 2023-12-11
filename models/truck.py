from datetime import *
from dataloaders import DistanceDataLoader, PackageDataLoader


class Truck:

    def __init__(self, distance_data_loader, package_data_loader, truck_id, max_packages=16, average_speed=18.0, miles_driven=0, assigned_driver_id=0):
        self.truck_id = truck_id
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.max_packages = max_packages
        self.average_speed = average_speed
        self.miles_driven = miles_driven
        self.package_list = []
        self.special_package_list = [] # Load special packages here first to then load into package_list

        current_date = datetime.now().date()
        self.earliest_leave_time = datetime.combine(current_date, time(hour=8, minute=0))
        self.can_leave_hub = False
        self.current_address_id = 0
        self.next_address_id = 0

    def calculate_eta(self, destination_address_id):
        current_location = self.current_address_id
        distance_to_destination = self.distance_data_loader.get_distance(current_location, destination_address_id)
        # Ensure that distance_to_destination is a numeric value
        if distance_to_destination is None:
            # Handle the case where the distance is not found
            return None

        travel_time = distance_to_destination / self.average_speed  # assuming speed is in miles per hour
        # Ensure travel_time is a valid number
        if travel_time is None or travel_time < 0:
            # Handle invalid travel time
            return None

        return self.earliest_leave_time + timedelta(hours=travel_time)

    def update_mileage_and_time(self, distance):
        self.miles_driven += distance

    def load_package(self, package_id):
        self.package_list.append(package_id)

    def unload_package(self, package_id):
        self.package_list.remove(package_id)

    def load_special_package(self, package_id):
        self.special_package_list.append(package_id)

    def unload_special_package(self, package_id):
        self.special_package_list.remove(package_id)

    def can_load_package(self, package):
        return len(self.package_list) < self.max_packages and package.required_truck in [0, self.truck_id]


    def set_earliest_leave_time(self):
        for package_id in self.package_list:
            package = self.package_data_loader.package_hash_table.search(package_id)
            if package and package.available_time > self.earliest_leave_time:
                self.earliest_leave_time = package.available_time

    def set_can_leave_hub(self, current_time):
        if current_time >= self.earliest_leave_time:
            self.can_leave_hub = True
            return True
        else:
            return False

    def deliver_packages(self, current_time):
        if self.can_leave_hub:
            next_package_id = self.package_list[0]

    def calculate_delivery_time(self, package):
        pass

    def is_full(self):
        return self.max_packages == len(self.package_list) # Only full if regular list is full


    def __repr__(self):
        return f"Truck ID: {self.truck_id} Current Packages: {self.package_list}"