class PackageSorter:
    def __init__(self, algorithm, package_data_loader, truck_manager):
        self.algorithm = algorithm  # Pass algorithm to this
        self.package_data_loader = package_data_loader
        self.package_hash_table = package_data_loader.package_hash_table
        self.truck_manager = truck_manager
        self.current_address_id = '0'
        self.package_id_list = self.package_hash_table.package_id_index
        self.next_package_distance_list = []

        self.sort_packages_onto_trucks()

    def sort_packages_onto_trucks(self):
        overall_distance = 0.0
        for truck in self.truck_manager.trucks:
            total_truck_distance = self.load_truck(truck)
            overall_distance += total_truck_distance
            self.print_truck_status(overall_distance, total_truck_distance, truck)

    def load_truck(self, truck):
        last_address_id = '0'
        total_truck_distance = 0.0
        while not truck.is_full() and self.package_id_list:
            next_package_id, next_package_distance, next_path = self.get_next_closest_package_path(last_address_id)
            package = self.package_hash_table.search(next_package_id)

            # Update the truck's path
            if next_path:
                # Skip the first element if it's the same as the last address to avoid duplication
                if next_path[0] == last_address_id:
                    next_path = next_path[1:]
                truck.truck_path_list.append(next_path)
                truck.truck_distance_list.append(next_package_distance)

            # Update the last address to the current package's address
            last_address_id = str(package.address_id)
            truck.load_package(next_package_id)
            self.package_id_list.remove(next_package_id)
            total_truck_distance += next_package_distance
        path_to_hub, distance_to_hub = self.algorithm.get_shortest_path(last_address_id, '0')
        # Remove the current address from the path to hub if it's the first element
        if path_to_hub and path_to_hub[0] == last_address_id:
            path_to_hub = path_to_hub[1:]
        truck.truck_path_list.append(path_to_hub)
        truck.truck_distance_list.append(distance_to_hub)
        total_truck_distance += distance_to_hub
        return total_truck_distance

    def print_truck_status(self, overall_distance, total_truck_distance, truck):
        print(f"Truck: {truck}\n"
              f"Path list: {truck.truck_path_list}\n"
              f"Distance list: {truck.truck_distance_list}\n"
              f"Estimated Truck Distance: {total_truck_distance:.1f}\n"
              f"Total Distance: {overall_distance:.1f}\n")

    # Returns correct next package but not next package path
    def get_next_closest_package_path(self, last_address_id):
        closest_package_id = None
        closest_distance = float('inf')
        closest_path = []

        for package_id in self.package_id_list:
            package = self.package_hash_table.search(package_id)
            path, path_distance = self.algorithm.get_shortest_path(last_address_id, str(package.address_id))

            if path_distance < closest_distance:
                closest_distance = path_distance
                closest_package_id = package_id
                closest_path = path
        return closest_package_id, closest_distance, closest_path


