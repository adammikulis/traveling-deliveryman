from models import address, ChainingHashTable, Package, Truck
from dataloaders import DistanceDataLoader, PackageDataLoader
from datetime import *


class SimulationManager:
    def __init__(self, distance_data_loader, package_data_loader, driver_manager, truck_manager, dispatcher, greedy, current_time, time_step):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.driver_manager = driver_manager
        self.truck_manager = truck_manager
        self.dispatcher = dispatcher
        self.greedy = greedy
        self.current_time = current_time  # Track the simulation time
        self.time_step = time_step  # Time step in seconds
        self.current_date = datetime.now().date()

    def advance_time(self):
        self.current_time = self.current_time + timedelta(seconds=self.time_step)
        self.update_truck_locations()
        self.update_package_statuses()

    def correct_package_address(self, package_data_loader, package_id, correct_address_id):
        package = package_data_loader.package_hash_table.search(package_id)
        package.address_id = correct_address_id
        package.wrong_address = False
    def update_truck_locations(self):
       for truck in self.truck_manager.trucks:
           truck.drive()

    def update_package_statuses(self):
        pass

    def get_package_status(self, package_id):
        pass

    def get_truck_status(self, truck_id):
        for truck in self.truck_manager.trucks:
            if truck.truck_id == truck_id:
                return truck.total_miles_driven, truck.package_list
        return None