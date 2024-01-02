from datetime import datetime, time

# This class implements the chosen algorithm to sort the packages onto trucks in most efficient order
class PackageManager:
    def __init__(self, algorithm, package_data_loader, truck_manager):
        self.algorithm = algorithm  # Pass algorithm to this
        self.package_data_loader = package_data_loader
        self.package_hash_table = package_data_loader.package_hash_table
        self.truck_manager = truck_manager
        self.package_id_list = self.package_hash_table.id_index
        self.early_deadline_package_id_list = []
        self.next_package_distance_list = []
        self.current_date = datetime.now().date()

        # Class initializes sorting without needing to call in main
        self.sort_packages_onto_trucks()


    # This implements the loading algorithm until the truck is full or all packages are loaded
    def load_truck(self, truck):
        while not truck.is_full() and (self.package_id_list or truck.special_package_id_list):
            self.load_truck_if_package_id(truck)
        # Sends trucks back to hub at the end of delivery
        self.append_hub_address_id_at_end(truck)

    # Gets called when truck is full or all possible packages have been loaded to send truck back to hub
    def append_hub_address_id_at_end(self, truck):
        path_to_hub, distance_to_hub = self.algorithm.get_shortest_path(str(truck.current_address_id), '0')
        truck.truck_path_list.append(path_to_hub)
        truck.truck_distance_list.append(distance_to_hub)
        truck.total_miles_driven += distance_to_hub

    # Used in load_truck
    def load_truck_if_package_id(self, truck):
        # Forces truck to prioritize special packages if combined lists reach truck's max capacity
        if len(truck.special_package_id_list) + len(truck.package_id_list) == truck.max_packages:
            next_package_id, next_package_distance, next_path = self.get_next_closest_package_id(truck, True)
            truck.unload_special_package_id_list(next_package_id)
        else:
            # Search both regular and special packages
            next_package_id, next_package_distance, next_path, is_package_special = self.get_next_combined_closest_package_id(truck)
            if is_package_special:
                truck.unload_special_package_id_list(next_package_id)
            else:
                self.package_id_list.remove(next_package_id)
        package = self.package_hash_table.search(next_package_id)
        package.assigned_truck_id = truck.truck_id
        # Update the truck's path
        if next_path:
            # Skip the first item if it's the same as the last address to avoid duplication
            if next_path[0] == truck.current_address_id:
                next_path = next_path[1:]
            truck.truck_path_list.append(next_path)
            truck.truck_distance_list.append(next_package_distance)
            truck.package_deadline_list.append(package.delivery_deadline)
        # Update the last address to the current package's address
        truck.load_package(next_package_id)
        truck.current_address_id = package.address_id
        truck.total_miles_driven += next_package_distance

    def print_truck_status(self, overall_distance, truck):
        print(f"Truck: {truck}\n"
              f"Path list: {truck.truck_path_list}\n"
              f"Distance list: {truck.truck_distance_list}\n"
              f"Estimated Truck Distance: {truck.total_miles_driven:.1f}\n"
              f"Total Distance: {overall_distance:.1f}\n")

    # Iterates packing algorithm through all trucks
    def sort_packages_onto_trucks(self):
        self.sort_special_packages_onto_trucks()
        overall_distance = 0.0
        for truck in self.truck_manager.trucks:
            self.load_truck(truck)  # Algorithm implemented here
            overall_distance += truck.total_miles_driven
            # self.print_truck_status(overall_distance, truck)

    # Uses algorithm to recall the shortest path
    def get_next_closest_package_id(self, truck, use_special_package_id_list):
        closest_package_id = None
        closest_distance = float('inf')
        closest_path = []
        closest_delivery_deadline = datetime.max  # Unused due to efficiency of pathing algorithm

        if use_special_package_id_list:
            package_id_list = truck.special_package_id_list
        else:
            package_id_list = self.package_id_list
        for package_id in package_id_list:
            package = self.package_hash_table.search(package_id)
            path, path_distance = self.algorithm.get_shortest_path(str(truck.current_address_id), str(package.address_id))
            if package.delivery_deadline < datetime.combine(self.current_date, time(12, 0)):
                self.early_deadline_package_id_list.append(package.package_id)
            if path_distance < closest_distance:
                closest_distance = path_distance
                closest_package_id = package_id
                closest_path = path
        return closest_package_id, closest_distance, closest_path

    # Returns closest package id of either global list or truck's special list
    def get_next_combined_closest_package_id(self, truck):
        special_distance_weight = .4  # Used to prioritize special packages by artificially reducing distance
        closest_regular_package_id, closest_regular_distance, closest_regular_path = self.get_next_closest_package_id(truck, False)
        closest_special_package_id, closest_special_distance, closest_special_path = self.get_next_closest_package_id(truck, True)

        # Logic to determine whether to choose a regular or special package
        if closest_regular_package_id is None:
            return closest_special_package_id, closest_special_distance, closest_special_path, True
        elif closest_special_package_id is None:
            return closest_regular_package_id, closest_regular_distance, closest_regular_path, False

        if closest_regular_distance < (closest_special_distance * special_distance_weight):  # Special distance is artificially lower using weight
            return closest_regular_package_id, closest_regular_distance, closest_regular_path, False
        else:
            return closest_special_package_id, closest_special_distance, closest_special_path, True

    # Populates trucks' special package list based on criteria
    def sort_special_packages_onto_trucks(self):
        # Load packages required by specific trucks
        for truck_id, package_ids in self.package_data_loader.package_required_trucks.items():
            for package_id in package_ids:
                if package_id in self.package_id_list:
                    self.truck_manager.trucks[truck_id - 1].load_special_package_id_list(package_id)
                    self.package_id_list.remove(package_id)

        # Load grouped packages
        for group_id, package_ids in self.package_data_loader.package_groups.items():
            # Default to the second truck for grouped packages (all arrive on-time this way)
            for package_id in package_ids:
                if package_id in self.package_id_list:
                    self.truck_manager.trucks[1].load_special_package_id_list(package_id)
                    self.package_id_list.remove(package_id)  # Remove from global package id list

        # Assign packages available after 8:00 AM or with a wrong address to truck 3
        available_time_cutoff = time(8, 0)
        for package_id in self.package_id_list:
            package = self.package_hash_table.search(package_id)
            if package.available_time.time() > available_time_cutoff or package.wrong_address:
                # Load onto Truck 3
                self.truck_manager.trucks[2].load_special_package_id_list(package_id)
                self.package_id_list.remove(package_id)  # Remove from the global package id list


    # Only needed if prioritizing by deadline, currently unused
    def normalize_deadline(self, deadline):

        start_time = datetime.combine(deadline.date(), time(8, 0))  # 8:00 AM
        end_time = datetime.combine(deadline.date(), time(17, 0))  # 5:00 PM

        # Total range in minutes
        total_range_minutes = (end_time - start_time).total_seconds() / 60

        # Deadline time in minutes from midnight
        deadline_minutes = (deadline - datetime.combine(deadline.date(), time(0, 0))).total_seconds() / 60

        # Start time in minutes from midnight
        start_time_minutes = (start_time - datetime.combine(start_time.date(), time(0, 0))).total_seconds() / 60

        # Normalize the deadline
        normalized_value = (start_time_minutes - deadline_minutes) / total_range_minutes
        normalized_value = min(max(normalized_value, 0), 1)

        return normalized_value