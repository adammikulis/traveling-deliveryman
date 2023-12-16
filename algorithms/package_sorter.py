class PackageSorter:
    def __init__(self, algorithm, package_data_loader, truck_manager):
        self.algorithm = algorithm  # Pass algorithm to this
        self.package_data_loader = package_data_loader
        self.package_hash_table = package_data_loader.package_hash_table
        self.truck_manager = truck_manager
        self.current_address_id = '0'
        self.package_id_list = self.package_hash_table.package_id_index
        self.next_package_distance_list = []

        # Class initializes sorting without needing to call in main
        self.sort_packages_onto_trucks()


    # This implements the pathing algorithm
    def load_truck(self, truck):
        last_address_id = '0'
        while not truck.is_full() and self.package_id_list:
            self.load_truck_if_package_id(truck)
        # Sends trucks back to hub at the end of delivery
        self.append_hub_address_id_at_end(last_address_id, truck)

    def append_hub_address_id_at_end(self, last_address_id, truck):
        path_to_hub, distance_to_hub = self.algorithm.get_shortest_path(last_address_id, '0')
        # Remove the current address from the path to hub if it's the first path element
        if path_to_hub and path_to_hub[0] == last_address_id:
            path_to_hub = path_to_hub[1:]
        truck.truck_path_list.append(path_to_hub)
        truck.truck_distance_list.append(distance_to_hub)
        truck.total_miles_driven += distance_to_hub

    # Used in load_truck
    def load_truck_if_package_id(self, truck):
        next_package_id, next_package_distance, next_path = self.get_next_closest_package_path(truck)
        package = self.package_hash_table.search(next_package_id)
        # Update the truck's path
        if next_path:
            # Skip the first item if it's the same as the last address to avoid duplication
            if next_path[0] == truck.current_address_id:
                next_path = next_path[1:]
            truck.truck_path_list.append(next_path)
            truck.truck_distance_list.append(next_package_distance)
        # Update the last address to the current package's address
        last_address_id = str(package.address_id)  # Graph labels are strings not ints like address_id
        truck.load_package(next_package_id)
        self.package_id_list.remove(next_package_id)
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
            self.print_truck_status(overall_distance, truck)

    # Uses algorithm to recall shortest path
    def get_next_closest_package_path(self, truck):
        closest_package_id = None
        closest_distance = float('inf')
        closest_path = []

        for package_id in self.package_id_list:
            package = self.package_hash_table.search(package_id)
            path, path_distance = self.algorithm.get_shortest_path(str(truck.current_address_id), str(package.address_id))

            if path_distance < closest_distance:
                closest_distance = path_distance
                closest_package_id = package_id
                closest_path = path
        return closest_package_id, closest_distance, closest_path

    def sort_special_packages_onto_trucks(self):
        # Load packages required by specific trucks
        for truck_id, package_ids in self.package_data_loader.package_required_trucks.items():
            for package_id in package_ids:
                if package_id in self.package_id_list:
                    self.truck_manager.trucks[truck_id - 1].load_special_package(package_id)
                    self.package_id_list.remove(package_id)

        # Load grouped packages
        for group_id, package_ids in self.package_data_loader.package_groups.items():
            # Default to the first truck for grouped packages (lowest mileage so far)
            for package_id in package_ids:
                if package_id in self.package_id_list:
                    self.truck_manager.trucks[0].load_special_package(package_id)
                    self.package_id_list.remove(package_id)  # Remove from global package id list
