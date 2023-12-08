from models import ChainingHashTable


class Truck:

    def __init__(self, truck_number=0, max_packages=16, average_speed=18, miles_driven=0):
        self.truck_number = truck_number
        self.max_packages = max_packages
        self.average_speed = average_speed
        self.miles_driven = miles_driven
        self.package_list = ChainingHashTable(max_packages)
