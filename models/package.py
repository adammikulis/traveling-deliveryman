from datetime import *

# This class creates packages and stores their metadata
class Package:
    def __init__(self, package_id=0, address_id=0, available_time=time(0, 0), delivery_deadline=time(0, 0),
                 weight=0, required_truck=0, delivery_group_id=0, wrong_address=False, address_available_time=time(0,0)):
        # package_hash_table columns
        self.package_id = package_id
        self.address_id = address_id
        self.weight = weight
        self.required_truck = required_truck  # Normalized from "special notes"
        self.delivery_group_id = delivery_group_id  # Normalized from "special notes"
        self.wrong_address = wrong_address  # Normalized from "special notes"

        # Convert everything to datetime
        self.current_date = datetime.now().date()
        self.available_time = datetime.combine(self.current_date, available_time)
        self.delivery_deadline = datetime.combine(self.current_date, delivery_deadline)
        self.address_available_time = datetime.combine(self.current_date, address_available_time)

        # Status variables
        self.assigned_truck_id = 0
        if self.available_time > datetime.combine(self.current_date, time(8,0)):
            self.status = "Not yet available"
        else:
            self.status = "At-hub"
        self.delivered_at = datetime.min
        self.delivered_on_time = False

    # Part B required lookup function
    def package_status_lookup(self):
        return self.delivery_deadline, self.address_id, self.weight, self.status, self.delivered_at  # address_id is referenced to obtain address, city, and zip code

    # Printable representation of object
    def __str__(self):

        # Returns current status with different overall output based on package status
        match self.status:
            case "Delivered":
                return f"Package ID: {self.package_id},\tStatus: Delivered to {self.address_id} at {self.delivered_at.strftime('%H:%M')}, by Truck {self.assigned_truck_id}, On-time: {self.delivered_on_time}"
            case "In-transit":
                return f"Package ID: {self.package_id},\tStatus: In-transit on Truck: {self.assigned_truck_id}"
            case "At-hub":
                return f"Package ID: {self.package_id},\tStatus: At-hub"

class CorrectedPackage:
    def __init__(self, package_id, correct_address_id, correction_time):
        self.package_id = package_id
        self.correct_address_id = correct_address_id
        self.correction_time = correction_time
