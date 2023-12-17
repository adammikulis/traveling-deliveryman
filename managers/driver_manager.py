from models import Driver

class DriverManager:

    def __init__(self, total_drivers):
        self.drivers = [Driver(i+1) for i in range(total_drivers)]

    def assign_driver_to_truck(self, driver_id, truck_id, truck_manager):
        driver = self.drivers[driver_id - 1]
        driver.assigned_truck_id = truck_id
        truck_manager.trucks[truck_id - 1].assigned_driver_id = driver_id

    def remove_driver_from_truck(self, driver_id, truck_manager):
        driver = self.drivers[driver_id - 1]
        if driver.assigned_truck_id is not None:
            truck_id = driver.assigned_truck_id
            driver.assigned_truck_id = None
            truck_manager.trucks[truck_id - 1].assigned_driver_id = None

    def assign_all_drivers_to_trucks(self, truck_manager):
        for driver in self.drivers:
            for truck in truck_manager.trucks:
                if truck.assigned_driver_id == 0:
                    self.assign_driver_to_truck(driver.driver_id, truck.truck_id, truck_manager)
                    break