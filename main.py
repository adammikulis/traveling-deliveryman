from datetime import time

from managers import TruckManager, DriverManager, DeliveryManager
from algorithms import Greedy

from dataloaders import DistanceDataLoader, PackageDataLoader

if __name__ == '__main__':

    package_data_loader = PackageDataLoader()
    package_data_filepath = "data/package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    distance_data_loader = DistanceDataLoader()
    distance_data_filepath = "data/distance_data.csv"
    distance_data_loader.load_distance_data(distance_data_filepath)

    # Initialize TruckManager and DriverManager
    num_trucks = 3
    truck_manager = TruckManager(num_trucks, distance_data_loader, package_data_loader)
    num_drivers = 2
    driver_manager = DriverManager(num_drivers)

    driver_manager.assign_driver_to_truck(1, 1, truck_manager)
    driver_manager.assign_driver_to_truck(2, 2, truck_manager)

    # Initialize greedy algorithm and DeliveryManager
    greedy = Greedy(distance_data_loader, package_data_loader)
    greedy.sort_packages_into_trucks(truck_manager)

    for truck in truck_manager.trucks:
        truck.set_earliest_leave_time()
        truck.set_can_leave_hub(time(8, 0))

        print(truck.earliest_leave_time)
        print(truck.can_leave_hub)
