class PackageSorter:
    def __init__(self, algorithm, package_data_loader, truck_manager):
        self.algorithm = algorithm  # Pass dijkstra to this

        self.package_data_loader = package_data_loader
        self.package_hash_table = package_data_loader.package_hash_table

        self.truck_manager = truck_manager
        self.current_address_id = '0'
        self.package_id_list = self.package_hash_table.package_id_index
        self.sort_packages_onto_trucks()

    def sort_packages_onto_trucks(self):
        for truck in self.truck_manager.trucks:
            #print(f"Truck: {truck.truck_id}")
            while not truck.is_full() and self.package_id_list:
                next_package_id = self.get_next_closest_package_id()
                # print(f"Next package id: {next_package_id}")

                if next_package_id is not None:
                    package = self.package_hash_table.search(next_package_id)
                    package.truck_id = truck.truck_id
                    truck.load_package(next_package_id)
                    self.package_id_list.remove(next_package_id)

            print(truck)

    def get_next_closest_package_id(self):
        closest_package_id = None
        closest_distance = float('inf')

        for package_id in self.package_id_list:
            package = self.package_hash_table.search(package_id)
            path, path_distance = self.algorithm.get_shortest_path(str(self.current_address_id),
                                                                   str(package.address_id))

            if path_distance < closest_distance:
                closest_distance = path_distance
                closest_package_id = package_id  # Use package_id instead of package.package_id

        # Update the current address only after finding the closest package
        if closest_package_id is not None:
            closest_package = self.package_hash_table.search(closest_package_id)
            self.current_address_id = closest_package.address_id

        return closest_package_id
