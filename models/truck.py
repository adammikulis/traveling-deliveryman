from datetime import *
from models import ChainingHashTable, Package
from dataloaders import DistanceDataLoader, PackageDataLoader


class Truck:

    def __init__(self, distance_data_loader, package_data_loader, truck_id, max_packages=16, average_speed=18.0):
        self.truck_id = truck_id
        self.distance_data_loader = distance_data_loader
        self.distance_table = self.distance_data_loader.distance_table
        self.package_data_loader = package_data_loader
        self.package_hash_table = self.package_data_loader.package_hash_table
        self.max_packages = max_packages
        self.average_speed = average_speed
        self.total_miles_driven = 0.0
        self.package_list = []
        self.special_package_list = [] # Load special packages here first to then load into package_list
        self.assigned_driver_id = 0
        self.current_date = datetime.now().date()
        self.current_address_id = 0
        self.next_address_id = 0
        self.next_address_distance = 0.0
        self.next_address_distance_driven = 0.0

    # def calculate_eta(self, destination_address_id):
    #     current_location = self.current_address_id
    #     distance_to_destination = self.distance_data_loader.get_distance(current_location, destination_address_id)
    #     # Ensure that distance_to_destination is a numeric value
    #     if distance_to_destination is None:
    #         # Handle the case where the distance is not found
    #         return None
    #
    #     travel_time = distance_to_destination / self.average_speed  # assuming speed is in miles per hour
    #     # Ensure travel_time is a valid number
    #     if travel_time is None or travel_time < 0:
    #         # Handle invalid travel time
    #         return None
    #
    #     return self.earliest_leave_time + timedelta(hours=travel_time)

    def drive(self):
        # Only drive if the truck has a driver
        if self.assigned_driver_id != 0:
            # Get the next_address_id if there is none
            if self.next_address_id is None:
                # Check if there are any packages left to deliver
                if self.package_list:
                    next_package_id = self.package_list[0]
                    next_package = self.package_hash_table.search(next_package_id)
                    self.next_address_id = next_package.address_id
                    self.next_address_distance = self.distance_data_loader.get_distance(self.current_address_id, self.next_address_id)
                # Send truck back to hub if package list is empty
                else:
                    self.next_address_id = 0
                    self.next_address_distance = self.distance_data_loader.get_distance(self.current_address_id, 0)

            if self.next_address_id is not None:
                print(f"Driving to {self.next_address_id}")
                drive_distance = self.average_speed / (60 * 60) # This utilizes a timestep of 1 second
                self.total_miles_driven += drive_distance
                self.next_address_distance_driven += drive_distance

            # If the truck reaches the next stop
            if self.next_address_distance_driven == self.next_address_distance:
                print(f"Arrived at {self.next_address_id}")
                self.current_address_id = self.next_address_id
                self.unload_package(self.package_list[0])



        # keep track of distance between current_address_id and next_address_id
        # advances with time and uses 18mph speed
        # if distance traveled == the calculated distance between the address ids then it has arrived
        # then calls self.deliver()
        pass

    def deliver(self):
        # drops off package
        # sets
        pass

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

    def deliver_packages(self, current_time):
        if self.can_leave_hub:
            next_package_id = self.package_list[0]

    def calculate_delivery_time(self, package):
        pass

    def is_full(self):
        return self.max_packages == len(self.package_list) # Only full if regular list is full


    def __repr__(self):
        return f"Truck ID: {self.truck_id} Driver: {self.assigned_driver_id} Current Packages: {self.package_list}"