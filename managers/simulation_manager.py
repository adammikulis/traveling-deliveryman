from datetime import *

from algorithms import DijkstraShortestPath
from dataloaders import GraphDataLoader, AddressDataLoader, PackageDataLoader
from managers import PackageManager, TruckManager, DriverManager


# This class runs the overall simulation
class SimulationManager:
    def __init__(self, num_drivers, num_trucks, start_time, end_time, time_step, corrected_packages):

        self.num_drivers = num_drivers
        self.num_trucks = num_trucks
        self.current_date = datetime.now().date()
        self.start_time = start_time
        self.current_time = datetime.combine(self.current_date, self.start_time)
        self.end_time = end_time
        self.end_date_time = datetime.combine(self.current_time, end_time)
        self.corrected_packages = corrected_packages
        self.time_step = time_step  # Time step in seconds

        self.graph_data_loader = GraphDataLoader('distance_data.csv')
        self.package_data_loader = PackageDataLoader('package_data.csv')
        self.address_data_loader = AddressDataLoader('address_data.csv')
        self.address_table = self.address_data_loader.address_table
        self.algorithm = DijkstraShortestPath(self.graph_data_loader)

        self.all_package_status_checks = []
        self.package_id_to_check = None
        self.status_check_time = None

        self.driver_manager = DriverManager(num_drivers)
        self.truck_manager = TruckManager(num_trucks, self.algorithm, self.package_data_loader, 16)
        self.package_manager = PackageManager(self.algorithm, self.package_data_loader, self.truck_manager)
        self.driver_manager.assign_all_drivers_to_trucks(self.truck_manager)

        for truck in self.truck_manager.trucks:
            truck.total_miles_driven = 0.0
        self.all_truck_miles_driven = 0.0

    # Reinitializes all parts of the simulation to use in __main__ loop
    def reset_simulation(self):
        self.__init__(self.num_drivers, self.num_trucks, self.start_time, self.end_time, self.time_step,
                      self.corrected_packages)

    # Advances time and truck locations by the time_step
    def advance_time(self):
        self.current_time = self.current_time + timedelta(0, self.time_step)
        self.update_truck_locations()

    # Corrects a package address
    def correct_package_address(self, corrected_package):
        if self.current_time == datetime.combine(self.current_date, corrected_package.correction_time):
            package = self.package_data_loader.package_hash_table.search(corrected_package.package_id)
            package.address_id = corrected_package.correct_address_id
            package.wrong_address = False

    # Runs during simulation loop to correct any packages at the designated time
    def correct_all_packages(self, corrected_packages):
        for corrected_package in corrected_packages:
            self.correct_package_address(corrected_package)

    # Make packages available at hub when they arrive
    def update_unarrived_packages(self):
        for package_id in self.package_data_loader.package_id_list:
            package = self.package_data_loader.package_hash_table.search(package_id)
            if package.status == "Not yet available" and package.available_time == self.current_time:
                package.status = "At-hub"

    # Move the trucks
    def update_truck_locations(self):
        self.all_truck_miles_driven = 0.0
        for truck in self.truck_manager.trucks:
            truck.drive_to_next_address_id(self.time_step, self.current_time)
            self.all_truck_miles_driven += truck.total_miles_driven

    # Loop for printing all package updates
    def print_all_package_status(self):
        all_packages_on_time = True
        print(f"\n*****ALL PACKAGE STATUS UPDATE***** Current time: {self.current_time.strftime('%H:%M')}")
        for package_id in self.package_data_loader.package_id_list:
            if not self.print_package_status(package_id):
                all_packages_on_time = False
        print(f"All truck miles driven: {self.all_truck_miles_driven:.1f}")
        print(f"All packages on-time: {all_packages_on_time}")

    # Used for status of a single package
    def check_package_status_at_time(self):
        if self.status_check_time and self.current_time == self.status_check_time:
            self.print_package_status(self.package_id_to_check)

    # Used for user-determined status reports, returns False if package is delivered late
    def print_package_status(self, package_id):
        package = self.package_data_loader.package_hash_table.search(package_id)
        delivery_deadline, address_id, weight, status, delivered_at = package.package_status_lookup()
        address = self.address_data_loader.get_address(package.address_id)
        street_address = address.street_address
        city = address.city
        zip_code = address.zip_code
        assigned_truck_id = package.assigned_truck_id
        delivered_at = package.delivered_at
        package_on_time = package.delivered_on_time
        available_time = package.available_time
        delivery_deadline = package.delivery_deadline
        weight = package.weight
        match status:
            case "Not yet available":
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {street_address} \t"
                    f"City: {city} \tZip Code: {zip_code} \tWeight: {weight} \tStatus: {status} \t"
                    f"Arriving at Hub: {available_time.strftime('%H:%M')}")
            case "At-hub":
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {street_address} \t"
                    f"City: {city} \tZip Code: {zip_code} \tWeight: {weight} \tStatus: {status} \t"
                    f"On Truck: {assigned_truck_id}")
            case "In-transit":
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {street_address} \t"
                    f"City: {city} \tZip Code: {zip_code} \tWeight: {weight} \tStatus: {status} \t"
                    f"On Truck: {assigned_truck_id}")
            case "Delivered":
                if not package_on_time:
                    return False
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {street_address} \t"
                    f"City: {city} \tZip Code: {zip_code} \tWeight: {weight} \tStatus: {status} "
                    f"at: {delivered_at.strftime('%H:%M')} \tOn-time: {package_on_time}")
        return True

    # Gets total miles driven and current package_id_list of a truck
    def get_truck_status(self, truck_id):
        for truck in self.truck_manager.trucks:
            if truck.truck_id == truck_id:
                return truck.total_miles_driven, truck.package_id_list
        return None

    # Assigns returning driver to next open truck
    def reassign_drivers(self):
        for truck in self.truck_manager.trucks[:-1]:
            if truck.finished_delivery_at_hub and self.truck_manager.trucks[-1].assigned_driver_id == 0:
                self.driver_manager.assign_driver_to_truck(truck.assigned_driver_id, self.truck_manager.trucks[-1].truck_id, self.truck_manager)
                truck.assigned_driver_id = 0

    # Print the statuses of all packages at set times
    def check_all_package_statuses(self, status_check_times):
        for status_check_time in status_check_times:
            if self.current_time == status_check_time:
                self.print_all_package_status()

    # This function is called every time-step during by simulate_delivery_day
    def simulate_deliveries(self):
        self.reassign_drivers()
        self.correct_all_packages(self.corrected_packages)
        self.update_unarrived_packages()
        self.check_all_package_statuses(self.all_package_status_checks)  # Will print all packages
        self.check_package_status_at_time()  # Will print just one package
        self.advance_time()

    # The main simulation loop that runs between designated times
    def simulate_delivery_day(self):
        while self.current_time <= self.end_date_time:
            self.simulate_deliveries()

    # Used for checking all packages
    def prompt_user_status_checks(self):
        num_status_checks = int(input("How many times would you like to check package status? "))
        for i in range(num_status_checks):
            self.append_status_check()

    # Used for checking a single package
    def prompt_user_individual_package_check(self):
        self.package_id_to_check = int(input("Which Package ID to check? "))
        status_check_time_str = input('What time to check (HH:MM)? ')
        hours, minutes = map(int, status_check_time_str.split(':'))
        self.status_check_time = datetime.combine(self.current_date, time(hours, minutes))

    # Adds to list of times to check all package statuses
    def append_status_check(self):
        status_check_time_str = input('What time to check (HH:MM)? ')
        hours, minutes = map(int, status_check_time_str.split(':'))
        status_check_date_time = datetime.combine(self.current_date, time(hours, minutes))
        self.all_package_status_checks.append(status_check_date_time)
