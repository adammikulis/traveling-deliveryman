
# Controls assignment of drivers to trucks
class Dispatcher:

    def __init__(self, driver_manager, truck_manager):
        self.driver_manager = driver_manager
        self.truck_manager = truck_manager
        self.assignments = {}

    def assign_driver_to_truck(self, driver_id, truck_id):
        self.assignments[driver_id] = truck_id
        # print(f"Driver {driver_id} assigned to Truck {truck_id}")

    def assign_drivers_to_trucks(self):
        for driver in self.driver_manager.drivers:
            for truck in self.truck_manager.trucks:
                if driver.driver_id not in self.assignments and truck.truck_id not in self.assignments.values():
                    self.assign_driver_to_truck(driver.driver_id, truck.truck_id)
                    break

    def get_truck_of_driver(self, driver_id):
        return self.assignments.get(driver_id, None)

    def get_driver_of_truck(self, truck_id):
        for driver_id, assigned_truck_id in self.assignments.items():
            if assigned_truck_id == truck_id:
                return driver_id
        return None