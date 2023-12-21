# Created by: Adam Mikulis
# Student ID: 002370265
# Program: Traveling Deliveryman
# Comments: This program optimizes package and delivery routes according to an algorithm
# Instructions: In a Command Prompt, navigate to the TravelingDeliveryman directory and run the command: python main.py

from datetime import *

from managers import TruckManager, DriverManager, SimulationManager, PackageManager
from algorithms import DijkstraShortestPath, Graph
from models import CorrectedPackage

from dataloaders import *





if __name__ == '__main__':

    # Load all data
    graph_data_loader = GraphDataLoader('distance_data.csv')
    address_data_loader = AddressDataLoader('address_data.csv')
    package_data_loader = PackageDataLoader('package_data.csv')

    # Initialize the algorithm
    algorithm = DijkstraShortestPath(graph_data_loader)

    # Initialize simulation
    num_drivers = 2
    num_trucks = 3
    start_time = time(8, 0)
    all_package_status_checks = [time(10, 00)]  # For quick testing
    corrected_packages = [CorrectedPackage(9, 19, time(10, 20))]

    simulation_manager = SimulationManager(graph_data_loader, package_data_loader, address_data_loader, algorithm, num_drivers, num_trucks, start_time, all_package_status_checks, corrected_packages, 1)

    # Prompt user for times to check package statuses
    # all_package_status_checks = []
    # num_status_checks = 3
    # print("What times would you like to check the package statuses?")
    # for i in range(num_status_checks):
    #     status_check_time_str = input('HH:MM: ')
    #     hours, minutes = map(int, status_check_time_str.split(':'))
    #     status_check_date_time = datetime.combine(current_date, time(hours, minutes))
    #     all_package_status_checks.append(status_check_date_time)


    # Simulation loop
    simulation_manager.simulate_delivery_day()