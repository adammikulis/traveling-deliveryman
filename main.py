# Created by: Adam Mikulis
# Student ID: 002370265
# Program: Traveling Deliveryman
# Comments: This program optimizes package and delivery routes according to an algorithm
# Instructions: In a Command Prompt, navigate to the TravelingDeliveryman directory and run the command: python main.py

from datetime import *
from managers import SimulationManager
from models import CorrectedPackage

if __name__ == '__main__':

    # Initialize simulation parameters
    num_drivers = 2
    num_trucks = 3
    start_time = time(8, 0)
    end_time = time(17,0)
    time_step = 1  # In seconds
    all_package_status_checks = [time(10, 00)]  # For quick testing
    corrected_packages = [CorrectedPackage(9, 19, time(10, 20))]

    # Initialize the simulation
    simulation_manager = SimulationManager(num_drivers, num_trucks, start_time, end_time, time_step, corrected_packages)
    while True:
        menu_choice = int(input(f"\n**********************************************************\n"
                                f"1. Print All Package Statuses and Total Mileage at Time(s)\n"
                                f"2. Print a Single Package Status at a Time\n"
                                f"3. Exit the Program\n"
                                f"**********************************************************\n"))
        match menu_choice:
            case 1:
                simulation_manager.prompt_user_status_checks()
                simulation_manager.simulate_delivery_day()
            case 2:
                simulation_manager.prompt_user_individual_package_check()
                simulation_manager.simulate_delivery_day()
            case 3:
                print("Goodbye and thank you!")
                break
        simulation_manager.reset_simulation()  # Needed to reset truck/package status in between menu selections
