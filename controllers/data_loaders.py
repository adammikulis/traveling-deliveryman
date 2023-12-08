from datetime import time, datetime
from models import Package
import csv


class DataLoaders:

    def __init__(self, hash_table):
        self.hash_table = hash_table

    def load_package_data(self, filename):
        with open(filename) as Packages:
            package_data = csv.reader(Packages, delimiter=',')
            next(package_data)  # skips header
            for package in package_data:
                package_id = int(package[0])
                address_id = int(package[1])
                available_time = datetime.strptime(package[2], '%H:%M').time()
                delivery_deadline = datetime.strptime(package[3], '%H:%M').time()
                weight = float(package[4])
                required_truck = int(package[5])
                delivery_group_id = int(package[6])
                wrong_address = bool(package[7])

                package_object = Package(package_id, address_id, available_time, delivery_deadline, weight, required_truck,
                                     delivery_group_id, wrong_address)
                self.hash_table.insert(package_object.package_id, package_object)
