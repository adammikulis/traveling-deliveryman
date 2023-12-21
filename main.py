# Created by: Adam Mikulis
# Student ID: 002370265
# Program: Traveling Deliveryman
# Comments: This program optimizes package and delivery routes according to an algorithm
# Instructions: In a Command Prompt, navigate to the TravelingDeliveryman directory and run the command: python main.py

from datetime import *

from managers import TruckManager, DriverManager, SimulationManager, PackageManager
from algorithms import DijkstraShortestPath, Graph

from dataloaders import *





if __name__ == '__main__':

    # Load all address distances
    graph = Graph()
    address_data_loader = AddressDataLoader()

    graph_data_loader = GraphDataLoader(graph)
    distance_data_filepath = "distance_data.csv"
    graph_data_loader.load_distance_data(distance_data_filepath)

    # Load all address names
    address_data_loader = AddressDataLoader()
    address_data_filepath = "address_data.csv"
    address_data_loader.load_address_data(address_data_filepath)

    # Load all packages
    package_data_loader = PackageDataLoader()
    package_data_filepath = "package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    # Initialize the algorithm
    algorithm = DijkstraShortestPath(graph)

    # Initialize TruckManager and DriverManager
    num_drivers = 2
    num_trucks = 3
    driver_manager = DriverManager(num_drivers)
    truck_manager = TruckManager(num_trucks, algorithm, package_data_loader, 16)
    driver_manager.assign_all_drivers_to_trucks(truck_manager)

    # Sort by algorithm
    package_manager = PackageManager(algorithm, package_data_loader, truck_manager)

    # Initialize simulation
    current_date = datetime.now().date()
    start_time = datetime.combine(current_date, time(8, 0))
    EOD = datetime.combine(current_date, time(17, 0))
    simulation_manager = SimulationManager(graph_data_loader, package_data_loader, address_data_loader, driver_manager, truck_manager, start_time, 1)

    # Prompt user for times to check package statuses
    # all_package_status_checks = []
    # num_status_checks = 3
    # print("What times would you like to check the package statuses?")
    # for i in range(num_status_checks):
    #     status_check_time_str = input('HH:MM: ')
    #     hours, minutes = map(int, status_check_time_str.split(':'))
    #     status_check_date_time = datetime.combine(current_date, time(hours, minutes))
    #     all_package_status_checks.append(status_check_date_time)
    all_package_status_checks = [datetime.combine(current_date, time(13, 00))]  # For quick testing

    # Simulation loop
    while simulation_manager.current_time <= EOD:
        simulation_manager.advance_time()

        # Reassigns the first driver that returns to hub to the final truck
        simulation_manager.reassign_trucks()

        # Used to correct a wrong package address at a specific time
        simulation_manager.correct_package_address(package_data_loader, 9, 19, time(10, 20))

        # Updates status of packages that haven't arrived yet
        simulation_manager.update_unarrived_packages()

        # Run status checks at prescribed times
        simulation_manager.check_all_package_statuses(all_package_status_checks)