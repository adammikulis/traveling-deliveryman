from datetime import *


# This class runs the overall simulation
class SimulationManager:
    def __init__(self, distance_data_loader, package_data_loader, address_table_loader, driver_manager, truck_manager, start_time, all_package_status_checks, corrected_packages, time_step):
        self.distance_data_loader = distance_data_loader
        self.package_data_loader = package_data_loader
        self.address_table_loader = address_table_loader
        self.address_table = address_table_loader.address_table
        self.driver_manager = driver_manager
        self.truck_manager = truck_manager
        self.time_step = time_step  # Time step in seconds


        self.current_time = start_time
        self.current_date = datetime.now().date()
        self.EOD = datetime.combine(self.current_date, time(17, 0))
        self.all_package_status_checks = all_package_status_checks
        self.corrected_packages = corrected_packages
        self.all_truck_miles_driven = 0.0

        self.reset_simulation()


    def reset_simulation(self):
        self.all_truck_miles_driven = 0.0
        for truck in self.truck_manager.trucks:
            truck.total_miles_driven = 0.0

    def advance_time(self):
        self.current_time = self.current_time + timedelta(0, self.time_step)
        self.update_truck_locations()

    def correct_package_address(self, corrected_package):
        if self.current_time == datetime.combine(self.current_date, corrected_package.correction_time):
            package = self.package_data_loader.package_hash_table.search(corrected_package.package_id)
            package.address_id = corrected_package.correct_address_id
            package.wrong_address = False

    def correct_all_packages(self, corrected_packages):
        for corrected_package in corrected_packages:
            self.correct_package_address(corrected_package)

    def update_unarrived_packages(self):
        for package_id in self.package_data_loader.package_id_list:
            package = self.package_data_loader.package_hash_table.search(package_id)
            if package.status == "Not yet available" and package.available_time == self.current_time:
                package.status = "At-hub"

    def update_truck_locations(self):
        self.all_truck_miles_driven = 0.0
        for truck in self.truck_manager.trucks:
            truck.drive_to_next_address_id(self.time_step, self.current_time)
            self.all_truck_miles_driven += truck.total_miles_driven
    def print_all_package_status(self):
        all_packages_on_time = True
        print(f"\n*****ALL PACKAGE STATUS UPDATE***** Current time: {self.current_time.strftime('%H:%M')}")
        for package_id in self.package_data_loader.package_id_list:
            if not self.print_package_status(package_id):
                all_packages_on_time = False
        print(f"All truck miles driven: {self.all_truck_miles_driven:.1f}")
        print(f"All packages on-time: {all_packages_on_time}")

    def print_package_status(self, package_id):
        package = self.package_data_loader.package_hash_table.search(package_id)
        address_id = package.address_id
        address = self.address_table[address_id]
        status = package.status
        assigned_truck_id = package.assigned_truck_id
        delivered_at = package.delivered_at
        package_on_time = package.delivered_on_time
        available_time = package.available_time
        delivery_deadline = package.delivery_deadline
        weight = package.weight
        match status:
            case "Not yet available":
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {address.street_address} \t"
                    f"City: {address.city} \tZip Code: {address.zip_code} \tWeight: {weight} \tStatus: {status} \t"
                    f"Arriving at Hub: {available_time.strftime('%H:%M')}")
            case "At-hub":
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {address.street_address} \t"
                    f"City: {address.city} \tZip Code: {address.zip_code} \tWeight: {weight} \tStatus: {status} \t"
                    f"On Truck: {assigned_truck_id}")
            case "In-transit":
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {address.street_address} \t"
                    f"City: {address.city} \tZip Code: {address.zip_code} \tWeight: {weight} \tStatus: {status} \t"
                    f"On Truck: {assigned_truck_id}")
            case "Delivered":
                if not package_on_time:
                    return False
                print(
                    f"Package ID: {package_id} \tDue: {delivery_deadline.strftime('%H:%M')} \tAddress: {address.street_address} \t"
                    f"City: {address.city} \tZip Code: {address.zip_code} \tWeight: {weight} \tStatus: {status} "
                    f"at: {delivered_at.strftime('%H:%M')} \tOn-time: {package_on_time}")
        return True

    def get_truck_status(self, truck_id):
        for truck in self.truck_manager.trucks:
            if truck.truck_id == truck_id:
                return truck.total_miles_driven, truck.package_id_list
        return None

    def reassign_trucks(self):
        for truck in self.truck_manager.trucks[:-1]:
            if truck.finished_delivery_at_hub and self.truck_manager.trucks[-1].assigned_driver_id == 0:
                self.driver_manager.assign_driver_to_truck(truck.assigned_driver_id, self.truck_manager.trucks[-1].truck_id, self.truck_manager)
                truck.assigned_driver_id = 0

    def check_all_package_statuses(self, status_checks):
        for status_check in status_checks:
            if self.current_time == status_check:
                self.print_all_package_status()

    def simulate_deliveries(self):
        self.advance_time()
        self.reassign_trucks()
        self.correct_all_packages(self.corrected_packages)
        self.update_unarrived_packages()
        self.check_all_package_statuses(self.all_package_status_checks)

    def simulate_delivery_day(self):
        while self.current_time <= self.EOD:
            self.simulate_deliveries()