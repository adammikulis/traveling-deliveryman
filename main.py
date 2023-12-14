from datetime import *

from managers import TruckManager, DriverManager, Dispatcher, SimulationManager
from algorithms import Greedy, DijkstraShortestPath, Graph

from dataloaders import *

if __name__ == '__main__':

    # Load all address distances
    graph = Graph()
    graph_data_loader = GraphDataLoader(graph)
    distance_data_filepath = "data/distance_data.csv"
    graph_data_loader.load_distance_data(distance_data_filepath)

    # Initialize the algorithm
    dijkstra = DijkstraShortestPath(graph)
    dijkstra.calculate_dijkstra_shortest_path()

    start_vertex_label = '0'
    end_vertex_label = '15'
    path = dijkstra.get_shortest_path(start_vertex_label, end_vertex_label)
    print("Shortest path:", path)


    # Load all address names
    address_data_loader = AddressDataLoader()
    address_data_filepath = "data/address_data.csv"
    address_data_loader.load_address_data(address_data_filepath)

    # Load all packages
    package_data_loader = PackageDataLoader()
    package_data_filepath = "data/package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    # Initialize TruckManager and DriverManager
    num_drivers = 2
    driver_manager = DriverManager(num_drivers)
    num_trucks = 3
    truck_manager = TruckManager(num_trucks, graph_data_loader, package_data_loader)

    # Assigns unassigned drivers to open trucks
    dispatcher = Dispatcher(driver_manager, truck_manager)
    dispatcher.assign_all_drivers_to_trucks()

    # Initialize greedy algorithm and DeliveryManager
    # greedy = Greedy(graph_data_loader, package_data_loader, truck_manager)
    # greedy.sort_packages_onto_trucks()

    # Initialize simulation
    current_date = datetime.now().date()
    start_time = datetime.combine(current_date, time(8, 0))
    EOD = datetime.combine(current_date, time(17, 0))

    status_checks = [datetime.combine(current_date, time(17, 0))]

    # simulation_manager = SimulationManager(graph_data_loader, package_data_loader, driver_manager,
    #                                        truck_manager, dispatcher, algorithm, start_time, 1)
    #
    # # Simulation loop
    # while simulation_manager.current_time <= EOD:
    #     simulation_manager.advance_time()
    #
    #     # Reassigns first driver that returns to final truck, this only works with n trucks / n-1 drivers
    #     for truck in truck_manager.trucks[:-1]:
    #         if truck.finished_delivery_at_hub and truck_manager.trucks[-1].assigned_driver_id == 0:
    #             # print(f"\nAssigning Driver {truck.assigned_driver_id} to Truck {truck_manager.trucks[-1].truck_id} at {simulation_manager.current_time.strftime("%H:%M")}")
    #             dispatcher.assign_driver_to_truck(truck.assigned_driver_id, truck_manager.trucks[-1].truck_id)
    #             truck.assigned_driver_id = 0
    #
    #     for status_check in status_checks:
    #         if simulation_manager.current_time == status_check:
    #             simulation_manager.print_all_package_status(package_data_loader, address_data_loader)
    #
    #     # Used to correct a package address
    #     if simulation_manager.current_time == datetime.combine(current_date, time(10, 20)):
    #         simulation_manager.correct_package_address(package_data_loader, 9, 19)