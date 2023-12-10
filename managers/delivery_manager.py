from models import PackageStatus

class DeliveryManager:
    def __init__(self, greedy_algorithm):
        self.greedy_algorithm = greedy_algorithm

    def deliver_packages(self):
        current_address_id = 0  # Starting address
        while True:
            next_closest_package = self.greedy_algorithm.get_next_closest_package(current_address_id)
            if next_closest_package is not None:
                self.deliver_package(next_closest_package)
                current_address_id = next_closest_package.address_id
                print(str(current_address_id))
            else:
                print("No more packages to deliver.")
                break

    def deliver_package(self, package):
        # Logic to mark the package as delivered
        package.status = PackageStatus.DELIVERED
        # Additional logic for delivery can be added here
