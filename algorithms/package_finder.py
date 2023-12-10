class PackageFinder:
    def __init__(self, distance_data_loader, package_data_loader):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader

    def get_next_closest_package(self, current_address_id):
        closest_distance = float('inf')
        closest_next_package = None
        for package_id in self.package_data_loader.package_ids:
            package = self.package_data_loader.package_hash_table.search(package_id)
            if package and package.address_id != current_address_id and package.status != PackageStatus.DELIVERED:
                distance = self.distance_data_loader.distance_table.get_distance(current_address_id, package.address_id)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_next_package = package
        return closest_next_package
