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
        # print(self.package_id_list)
        overall_distance = 0.0
        for truck in self.truck_manager.trucks:
            last_address_id = '0'
            total_truck_distance = 0.0

            while not truck.is_full() and self.package_id_list:
                next_package_id, next_package_distance, path = self.get_next_closest_package_path(last_address_id)
                package = self.package_hash_table.search(next_package_id)
                print(f"Next closest package from {last_address_id}: {next_package_id} at {package.address_id}")


                # Update the truck's path
                if path:
                    # Skip the first element if it's the same as the last address to avoid duplication
                    if path[0] == last_address_id:
                        truck.truck_path_list.extend(path[1:])
                    else:
                        truck.truck_path_list.extend(path)

                # Update the last address to the current package's address
                last_address_id = str(package.address_id)
                truck.load_package(next_package_id)
                self.package_id_list.remove(next_package_id)
                total_truck_distance += next_package_distance

            overall_distance += total_truck_distance
            print(f"Truck: {truck}\n"
                  f"Path list: {truck.truck_path_list}\n"
                  f"Estimated Truck Distance: {total_truck_distance}\n"
                  f"Total Distance: {overall_distance}\n")

    def get_next_closest_package_path(self, last_address_id):
        closest_package_id = None
        closest_distance = float('inf')

        for package_id in self.package_id_list:
            package = self.package_hash_table.search(package_id)
            path, path_distance = self.algorithm.get_shortest_path(last_address_id, str(package.address_id))

            if path_distance < closest_distance:
                closest_distance = path_distance
                closest_package_id = package_id
        return closest_package_id, closest_distance, path


