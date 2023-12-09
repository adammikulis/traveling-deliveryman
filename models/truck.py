class Truck:

    def __init__(self, truck_id=None, max_packages=16, average_speed=18, miles_driven=0, assigned_driver_id=None):
        self.truck_id = truck_id
        self.max_packages = max_packages
        self.average_speed = average_speed
        self.miles_driven = miles_driven
        self.package_list = []
        self.driver_id = 0

    def load_package(self, package_id):
        self.package_list.append(package_id)

    def unload_package(self, package_id):
        self.package_list.remove(package_id)


    def __repr__(self):
        return f"Truck ID: {self.truck_id} Current Packages: {self.package_list}"