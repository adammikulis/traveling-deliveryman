from models import Address, ChainingHashTable, Package, Truck
from dataloaders import GraphDataLoader, PackageDataLoader
from datetime import *

# This class runs the overall simulation
class SimulationManager:
    def __init__(self, distance_data_loader, package_data_loader, address_table_loader, driver_manager, truck_manager, start_time, time_step):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.address_table_loader = address_table_loader
        self.address_table = address_table_loader.address_table
        self.driver_manager = driver_manager
        self.truck_manager = truck_manager
        self.current_time = start_time
        self.time_step = time_step  # Time step in seconds
        self.current_date = datetime.now().date()
        self.all_truck_miles_driven = 0.0

        # Clears out current odometer for start of simulation
        for truck in truck_manager.trucks:
            truck.total_miles_driven = 0.0

    def advance_time(self):
        self.current_time = self.current_time + timedelta(0, self.time_step)
        self.update_truck_locations()

    def correct_package_address(self, package_data_loader, package_id, correct_address_id):
        package = package_data_loader.package_hash_table.search(package_id)
        package.address_id = correct_address_id
        package.wrong_address = False
    def update_truck_locations(self):
        self.all_truck_miles_driven = 0.0
        for truck in self.truck_manager.trucks:
            truck.drive_to_next_address_id(self.time_step, self.current_time)
            self.all_truck_miles_driven += truck.total_miles_driven

    def print_all_package_status(self):
        all_packages_on_time = True
        print(f"\n*****STATUS UPDATE***** Current time: {self.current_time.strftime("%H:%M")}")
        for package_id in self.package_data_loader.package_id_list:
            package = self.package_data_loader.package_hash_table.search(package_id)
            # print(package.package_status_lookup(self.address_table_loader))
            address_id = package.address_id
            address = self.address_table[address_id]
            status = package.status
            assigned_truck_id = package.assigned_truck_id
            delivered_at = package.delivered_at
            package_on_time = package.delivered_on_time
            available_time = package.available_time
            delivery_deadline = package.delivery_deadline

            match status:
                case "Not yet available":
                    print(f"Package ID: {package_id} \tStatus: {status} \tArriving at Hub: {available_time.strftime("%H:%M")} \tDue: {delivery_deadline.strftime("%H:%M")}")
                case "At-hub":
                    print(f"Package ID: {package_id} \tStatus: {status} \ton Truck: {assigned_truck_id} \tDue: {delivery_deadline.strftime("%H:%M")}")
                case "In-transit":
                    print(f"Package ID: {package_id} \tStatus: {status} \tTo: {address.location_name} by Truck: {assigned_truck_id} \tDue: {delivery_deadline.strftime("%H:%M")}")
                case "Delivered":
                    if package_on_time == False:
                        print(f"Late package: {package_id}")
                        all_packages_on_time = False
                    print(f"Package ID: {package_id} \tStatus: {status} \tTo: {address.location_name} \tby Truck: {assigned_truck_id} \tAt: {delivered_at.strftime("%H:%M")}")
        print(f"All truck miles driven: {self.all_truck_miles_driven:.1f}")
        print(f"All packages on-time: {all_packages_on_time}")


    def get_truck_status(self, truck_id):
        for truck in self.truck_manager.trucks:
            if truck.truck_id == truck_id:
                return truck.total_miles_driven, truck.package_id_list
        return None