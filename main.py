from datetime import *

from managers import TruckManager, DriverManager, Dispatcher, SimulationManager
from algorithms import Greedy

from dataloaders import DistanceDataLoader, PackageDataLoader

if __name__ == '__main__':

    # Load all address distances
    distance_data_loader = DistanceDataLoader()
    distance_data_filepath = "data/distance_data.csv"
    distance_data_loader.load_distance_data(distance_data_filepath)

    # Load all packages
    package_data_loader = PackageDataLoader()
    package_data_filepath = "data/package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    # Initialize TruckManager and DriverManager
    num_drivers = 2
    driver_manager = DriverManager(num_drivers)
    num_trucks = 3
    truck_manager = TruckManager(num_trucks, distance_data_loader, package_data_loader)

    # Assigns unassigned drivers to open trucks
    dispatcher = Dispatcher(driver_manager, truck_manager)
    dispatcher.assign_drivers_to_trucks()

    # Initialize greedy algorithm and DeliveryManager
    greedy = Greedy(distance_data_loader, package_data_loader, truck_manager)
    greedy.sort_packages_into_trucks()

    # Initialize simulation
    current_date = datetime.now().date()
    start_time = datetime.combine(current_date, time(8, 0))
    EOD = datetime.combine(current_date, time(hour=17, minute=0))
    simulation_manager = SimulationManager(distance_data_loader, package_data_loader, driver_manager,
                                           truck_manager, dispatcher, greedy, start_time, 1)

    while simulation_manager.current_time <= EOD:
        # print(f"The time is: {simulation_manager.current_time}")

        # Used to correct a package address
        if simulation_manager.current_time == datetime.combine(current_date, time(10, 20)):
            simulation_manager.correct_package_address(package_data_loader, 9, 19)


        simulation_manager.advance_time()
