from models import address, ChainingHashTable, Package, Truck
from dataloaders import DistanceDataLoader, PackageDataLoader
from datetime import datetime, timedelta

class SimulationManager:
    def __init__(self, distance_data_loader, package_data_loader, truck_manager, driver_manager, dispatcher, greedy, current_time, time_step):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.truck_manager = truck_manager
        self.driver_manager = driver_manager
        self.dispatcher = dispatcher
        self.greedy = greedy
        self.current_time = current_time  # Track the simulation time
        self.time_step = time_step  # Time step in seconds

    def advance_time(self):
        self.current_time = self.current_time + timedelta(seconds=self.time_step)
        self.update_truck_locations()
        self.update_package_statuses()

    def update_truck_locations(self):
       pass

    def update_package_statuses(self):
        pass

    def get_package_status(self, package_id):
        pass

    def get_truck_status(self, truck_id):
        for truck in self.truck_manager.trucks:
            if truck.truck_id == truck_id:
                return truck.miles_driven, truck.package_list
        return None