
# Controls assignment of drivers to trucks
class Dispatcher:

    def __init__(self, driver_manager, truck_manager):
        self.driver_manager = driver_manager
        self.truck_manager = truck_manager

    def assign_driver_to_truck(self, driver_id, truck_id):
        self.driver_manager.assign_driver_to_truck(driver_id, truck_id, self.truck_manager)

    def assign_all_drivers_to_trucks(self):
        for driver in self.driver_manager.drivers:
            for truck in self.truck_manager.trucks:
                if truck.assigned_driver_id == 0:
                    self.assign_driver_to_truck(driver.driver_id, truck.truck_id)
                    break