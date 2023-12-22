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

    # Initialize simulation parameters
    num_drivers = 2
    num_trucks = 3
    start_time = time(8, 0)
    end_time = time(17,0)
    all_package_status_checks = [time(10, 00)]  # For quick testing
    corrected_packages = [CorrectedPackage(9, 19, time(10, 20))]

    # Initialize the simulation
    simulation_manager = SimulationManager(num_drivers, num_trucks, start_time, end_time, 1, corrected_packages)
    menu_choice = None
    while menu_choice != 4:
        menu_choice = int(input(f"***************************************\n"
                                f"1. Print All Package Status and Total Mileage\n"
                                f"2. Get a Single Package Status with a Time\n"
                                f"3. Get All Package Status with a Time\n"
                                f"4. Exit the Program\n"
                                f"***************************************\n"))

        match menu_choice:
            case 1:
                simulation_manager.prompt_user_status_checks()
                simulation_manager.simulate_delivery_day()
            case 2:
                simulation_manager.prompt_user_individual_package_check()
                simulation_manager.simulate_delivery_day()