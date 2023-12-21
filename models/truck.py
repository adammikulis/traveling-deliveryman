from datetime import *

# This class creates the trucks that navigate from location-to-location to unload their packages
# Truck behavior is encapsulated and can drive/navigate on their own
class Truck:

    def __init__(self, truck_id, algorithm, package_data_loader, max_packages=16, average_speed=18.0):
        self.truck_id = truck_id
        self.algorithm = algorithm
        self.package_data_loader = package_data_loader
        self.package_hash_table = self.package_data_loader.package_hash_table
        self.max_packages = max_packages
        self.average_speed = average_speed
        self.total_miles_driven = 0.0

        self.package_id_list = []
        self.special_package_id_list = []  # Load special packages here first to then load into package_id_list
        self.truck_path_list = []  # For printing/debugging
        self.truck_distance_list = []  # For printing/debugging
        self.package_available_time_list = []  # For printing/debugging
        self.package_deadline_list = []  # For printing/debugging

        self.assigned_driver_id = 0
        self.current_date = datetime.now().date()
        self.current_address_id = 0
        self.next_address_id = None
        self.next_address_distance = 0.0
        self.next_address_distance_driven = 0.0
        self.next_address_path = []
        self.finished_delivery_at_hub = False

    # This gets executed when the truck has a driver and more packages to deliver
    def drive_to_next_address_id(self, time_step, current_time):

        # Only drive if the truck has a driver and isn't finished all deliveries
        if self.truck_has_driver() and not self.finished_delivery_at_hub:
            # If there are packages left to deliver
            if self.package_id_list:
                for package_id in self.package_id_list:
                    package = self.package_hash_table.search(package_id)
                    package.status = "In-transit"
            # Get the next_address_id if there is none
                if self.next_address_id is None:
                    next_package_id = self.package_id_list[0]
                    next_package = self.package_hash_table.search(next_package_id)
                    self.next_address_id = next_package.address_id

                    # Deliver the package if already at the current destination
                    if self.current_address_id == self.next_address_id:
                        self.deliver_package(next_package_id, current_time)
                    else:
                        # print(f"Truck {self.truck_id} with Driver {self.assigned_driver_id} driving to {self.next_address_id}")
                        self.next_address_path, self.next_address_distance = self.algorithm.get_shortest_path(str(self.current_address_id), str(self.next_address_id))

            # Send truck back to hub if package list is empty
            else:
                self.next_address_id = 0
                # print(f"Truck {self.truck_id} with Driver {self.assigned_driver_id} driving to back to hub")
                self.next_address_path, self.next_address_distance = self.algorithm.get_shortest_path(str(self.current_address_id), str(self.next_address_id))

            # Deliver the package and reset variables if truck arrives at next location
            if self.next_address_distance_driven >= self.next_address_distance:
                # print(f"Truck {self.truck_id} arrived at {self.next_address_id}")
                # Only try to deliver if there is a package
                self.current_address_id = self.next_address_id
                if self.package_id_list:
                    self.deliver_package(self.package_id_list[0], current_time)

                elif not self.package_id_list and self.current_address_id == 0:
                    # print(f"\nTruck {self.truck_id} arrived at depot at {current_time.strftime('%H:%M')} Total truck miles: {self.total_miles_driven:.1f}\n")
                    self.next_address_id = None
                    self.finished_delivery_at_hub = True

            # This advances the simulation
            self.simulate_drive(time_step)

    def truck_has_driver(self):
        return self.assigned_driver_id != 0

    # Advance the truck in the simulation by the time_step
    def simulate_drive(self, time_step):
        drive_distance = (self.average_speed * time_step) / 3600
        self.total_miles_driven += drive_distance
        self.next_address_distance_driven += drive_distance

    def load_package(self, package_id):
        self.package_id_list.append(package_id)

    def unload_package(self, package_id):
        self.package_id_list.remove(package_id)

    # Deliver package when truck reaches the address
    def deliver_package(self, package_id, current_time):
        self.current_address_id = self.next_address_id
        self.unload_package(package_id)
        package = self.package_hash_table.search(package_id)
        package.status = "Delivered"
        package.delivered_at = current_time
        package.delivered_on_time = current_time <= package.delivery_deadline
        self.next_address_id = None
        self.next_address_distance_driven = 0.0
        # print(f"Package: {package_id}\tdelivered to Address: {self.current_address_id} \t "
        #       f"by Truck: {self.truck_id} at {current_time.strftime('%H:%M')} "
        #       f"Due: {package.delivery_deadline}\t On-time: {package.delivered_on_time} "
        #       f"Truck miles: {self.total_miles_driven:.1f}")

    # Add a package to the truck's individual special package id list
    def load_special_package_id_list(self, package_id):
        self.special_package_id_list.append(package_id)

    # Remove a package from the truck's individual special package id list
    def unload_special_package_id_list(self, package_id):
        self.special_package_id_list.remove(package_id)

    def can_load_package(self, package):
        return len(self.package_id_list) < self.max_packages and package.required_truck in [0, self.truck_id]

    def is_full(self):
        return self.max_packages == len(self.package_id_list) # Only full if regular list is full

    # No longer needed due to route optimization
    # def calculate_eta(self, destination_address_id):
    #     current_location = self.current_address_id
    #     distance_to_destination = self.graph_data_loader.get_distance(current_location, destination_address_id)
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

    def __str__(self):
        address_delivery_list = []
        delivery_deadline_list = []
        for package_id in self.package_id_list:
            package = self.package_hash_table.search(package_id)
            address_id = package.address_id
            delivery_deadline = package.delivery_deadline
            self.package_available_time_list.append(package.available_time.strftime('%H:%M'))
            address_delivery_list.append(address_id)
            delivery_deadline_list.append(delivery_deadline.strftime('%H:%M'))
        return (f"Truck ID: {self.truck_id} Driver: {self.assigned_driver_id} "
                f"\nCurrent Packages: {self.package_id_list}"
                # f"\nSpecial Packages: {self.special_package_id_list}"
                f"\nPackage Addresses: {address_delivery_list}"
                f"\nAvailable Time: {self.package_available_time_list}"
                f"\nDelivery Deadline: {delivery_deadline_list}")