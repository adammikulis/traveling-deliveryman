from models import PackageStatus

class DeliveryManager:
    def __init__(self, greedy_algorithm):
        self.greedy_algorithm = greedy_algorithm

    def deliver_packages(self, starting_address=0):
        current_address_id = starting_address  # Starting address
        while True:
            next_closest_package = self.greedy_algorithm.get_next_closest_package(current_address_id)
            if next_closest_package is not None:
                self.deliver_package(next_closest_package)
                current_address_id = next_closest_package.address_id
                print(f"Package: {next_closest_package.package_id}, Address: {next_closest_package.address_id}, Truck: {next_closest_package.truck_id}")
            else:
                print("No more packages to deliver.")
                break

    def deliver_package(self, package):

        package.status = PackageStatus.DELIVERED

