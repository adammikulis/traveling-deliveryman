from managers import TruckManager, DriverManager
from models.truck import Truck
from models import Package

from dataloaders import DistanceDataLoader, PackageDataLoader

if __name__ == '__main__':

    num_trucks = 3
    num_drivers = 2
    # Create and fill package data loader
    package_data_loader = PackageDataLoader()
    package_data_filepath = "data/package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    # Create and fill distance data loader
    distance_data_loader = DistanceDataLoader()
    distance_data_filepath = "data/distance_data.csv"
    distance_data_loader.load_distance_data(distance_data_filepath)

    # all_distances = distance_data_loader.distance_table.get_all_distances()
    # for distance in all_distances:
    #     print(distance)
    # print(package_data_loader.package_hash_table.table)

    truck_list = TruckManager(num_trucks)
    driver_list = DriverManager(num_drivers)
    truck_list.load_package_into_truck(1, 4)
    print(truck_list.trucks)