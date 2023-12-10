from managers import TruckManager, DriverManager
from models.truck import Truck
from models import Package
from algorithms import Greedy

from dataloaders import DistanceDataLoader, PackageDataLoader

if __name__ == '__main__':

    num_trucks = 3
    num_drivers = 2
    truck_list = TruckManager(num_trucks)
    driver_list = DriverManager(num_drivers)

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

    greedy = Greedy()
    current_address_id = 0  # Starting address
    total_distance = 0

    while True:
        next_closest_package, distance = greedy.get_next_closest_package(current_address_id, package_data_loader, distance_data_loader)

        if next_closest_package is not None:
            total_distance += distance
            print(
                f"Current Address: {current_address_id}, \tNext address: {next_closest_package.address_id},\t Next package: {next_closest_package.package_id}, \tDistance: {distance}, \tTotal Distance: {"%.1f" % total_distance}")
            current_address_id = next_closest_package.address_id
        else:
            print("No more packages to deliver.")
            break

