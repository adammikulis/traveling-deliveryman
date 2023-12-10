from managers import TruckManager, DriverManager, DeliveryManager
from models.truck import Truck
from models import Package
from algorithms import Greedy, PackageFinder

from dataloaders import DistanceDataLoader, PackageDataLoader

if __name__ == '__main__':
    # Existing code for creating and filling package and distance data loaders
    package_data_loader = PackageDataLoader()
    package_data_filepath = "data/package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    distance_data_loader = DistanceDataLoader()
    distance_data_filepath = "data/distance_data.csv"
    distance_data_loader.load_distance_data(distance_data_filepath)

    # Initialize PackageFinder with the package and distance data loaders
    package_finder = PackageFinder(distance_data_loader, package_data_loader)

    # Initialize TruckManager and DriverManager
    num_trucks = 3
    truck_list = TruckManager(num_trucks)
    num_drivers = 2
    driver_list = DriverManager(num_drivers)

    # Delivery loop
    greedy = Greedy(distance_data_loader, package_data_loader)
    delivery_manager = DeliveryManager(greedy)

    # Start the delivery process
    delivery_manager.deliver_packages()