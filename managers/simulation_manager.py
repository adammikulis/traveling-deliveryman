from models import Address, PackageHashTable, Package, Truck
from dataloaders import GraphDataLoader, PackageDataLoader
from datetime import *


class SimulationManager:
    def __init__(self, distance_data_loader, package_data_loader, driver_manager, truck_manager, dispatcher, greedy, start_time, time_step):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.driver_manager = driver_manager
        self.truck_manager = truck_manager
        self.dispatcher = dispatcher
        self.greedy = greedy
        self.current_time = start_time
        self.time_step = time_step  # Time step in seconds
        self.current_date = datetime.now().date()
        self.all_truck_miles_driven = 0.0

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

    def print_all_package_status(self, package_data_loader, address_data_loader):
        overall_status = True
        print(f"\n***STATUS UPDATE*** Current time: {self.current_time.strftime("%H:%M")}")
        print(f"All truck miles driven: {self.all_truck_miles_driven:.1f}")
        for package_id in package_data_loader.package_id_list:
            address_id, truck_id, status, delivered_at, delivered_on_time = package_data_loader.return_all_package_info(
                package_id)
            address = address_data_loader.get_address(address_id)
            # match status:
            #     case "Delivered":
            #         print(
            #             f"Package ID: {package_id},\tStatus: Delivered to {address.street_address}\tat {delivered_at.strftime("%H:%M")},\tby Truck {truck_id},\tOn-time: {delivered_on_time}")
            #     case "In-transit":
            #         print(f"Package ID: {package_id},\tStatus: In-transit on Truck: {truck_id}")
            #     case "At-hub":
            #         print(f"Package ID: {package_id},\tStatus: At-hub")
            if not delivered_on_time:
                overall_status = False
        print(f"All packages delivered on-time: {overall_status}")


    def get_truck_status(self, truck_id):
        for truck in self.truck_manager.trucks:
            if truck.truck_id == truck_id:
                return truck.total_miles_driven, truck.package_id_list
        return None