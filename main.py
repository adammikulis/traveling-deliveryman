from datetime import *

from managers import TruckManager, DriverManager, Dispatcher, SimulationManager
from algorithms import DijkstraShortestPath, Graph, PackageSorter

from dataloaders import *

if __name__ == '__main__':

    # Load all address distances
    graph = Graph()
    graph_data_loader = GraphDataLoader(graph)
    distance_data_filepath = "data/distance_data.csv"
    graph_data_loader.load_distance_data(distance_data_filepath)

    # Load all address names
    address_data_loader = AddressDataLoader()
    address_data_filepath = "data/address_data.csv"
    address_data_loader.load_address_data(address_data_filepath)

    # Load all packages
    package_data_loader = PackageDataLoader()
    package_data_filepath = "data/package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    # Initialize the algorithm
    algorithm = DijkstraShortestPath(graph)

    # Initialize TruckManager and DriverManager
    num_drivers = 2
    driver_manager = DriverManager(num_drivers)
    num_trucks = 3
    truck_manager = TruckManager(num_trucks, algorithm, package_data_loader, 14)

    # Assigns unassigned drivers to open trucks
    dispatcher = Dispatcher(driver_manager, truck_manager)
    dispatcher.assign_all_drivers_to_trucks()

    # Sort by algorithm
    package_sorter = PackageSorter(algorithm, package_data_loader, truck_manager)

    # Initialize simulation
    current_date = datetime.now().date()
    start_time = datetime.combine(current_date, time(8, 0))
    EOD = datetime.combine(current_date, time(17, 0))



    simulation_manager = SimulationManager(graph_data_loader, package_data_loader, driver_manager, truck_manager, dispatcher, start_time, 1)

    # status_checks = []
    # num_status_checks = 3
    # for i in range(num_status_checks):
    #     status_check_time_str = input("What time to check status (HH:MM): ")
    #     hours, minutes = map(int, status_check_time_str.split(':'))
    #     status_check_date_time = datetime.combine(current_date, time(hours, minutes))
    #     status_checks.append(status_check_date_time)

    status_checks = [datetime.combine(current_date,time(9,5))]

    # Simulation loop
    while simulation_manager.current_time <= EOD:
        for status_check in status_checks:
            if simulation_manager.current_time == status_check:
                simulation_manager.print_all_package_status(package_data_loader, address_data_loader)

        # Reassigns first driver that returns to final truck
        for truck in truck_manager.trucks[:-1]:
            if truck.finished_delivery_at_hub and truck_manager.trucks[-1].assigned_driver_id == 0:
                # print(f"\nAssigning Driver {truck.assigned_driver_id} to Truck {truck_manager.trucks[-1].truck_id} at {simulation_manager.current_time.strftime("%H:%M")}")
                dispatcher.assign_driver_to_truck(truck.assigned_driver_id, truck_manager.trucks[-1].truck_id)
                truck.assigned_driver_id = 0


        # Used to correct a package address
        if simulation_manager.current_time == datetime.combine(current_date, time(10, 20)):
            simulation_manager.correct_package_address(package_data_loader, 9, 19)

        simulation_manager.advance_time()