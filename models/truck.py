class Truck:
    max_packages = 16
    average_speed = 18

    def __init__(self, truck_number=0, package_list=[]):
        self.truck_number = truck_number
        self.package_list = package_list