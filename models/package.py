from enum import Enum

class PackageStatus(Enum):
    AT_HUB = "At-hub"
    IN_TRANSIT = "In-transit"
    DELIVERED = "Delivered"


class Package:
    def __init__(self, package_id=0, address="", city="", state="", zip=0, available_time=0, delivery_deadline=0,
                 mass=0, required_truck=0, wrong_address=False, delivered_with=[], status=PackageStatus.AT_HUB):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.available_time = available_time
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.required_truck = required_truck
        self.wrong_address = wrong_address
        self.delivered_with = delivered_with
        self.status = status

    def set_package_id(self, number):
        self.package_id = number

    def get_package_id(self):
        return self.package_id

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status.value