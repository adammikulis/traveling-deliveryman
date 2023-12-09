from enum import Enum
from datetime import *


class PackageStatus(Enum):
    AT_HUB = "At-hub"
    IN_TRANSIT = "In-transit"
    DELIVERED = "Delivered"


class Package:
    def __init__(self, package_id=0, address_id=0, available_time=time(0, 0), delivery_deadline=time(0, 0),
                 weight=0, required_truck=0, delivery_group_id=0, wrong_address=False):
        # package_table columns
        self.package_id = package_id
        self.address_id = address_id
        self.available_time = available_time
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.required_truck = required_truck
        self.delivery_group_id = delivery_group_id
        self.wrong_address = wrong_address

        # status variables
        self.truck_id = 0
        self.package_status = PackageStatus.AT_HUB
        self.delivered_at = time(0, 0)

    # Printable representation of object
    def __repr__(self):

        # Returns current package_status with different overall output based on package status
        match self.package_status:
            case PackageStatus.DELIVERED:
                return f"Package ID:{self.package_id}, Status: {self.package_status.value} at {self.delivered_at})"
            case PackageStatus.IN_TRANSIT:
                return f"Package ID:{self.package_id}, Status: {self.package_status.value} on Truck: {self.truck_id})"
            case PackageStatus.AT_HUB:
                return f"Package ID:{self.package_id}, Status: {self.package_status.value})"