class SimulationManager:
    def __init__(self, truck_manager, delivery_manager, time_step=1):
        self.truck_manager = truck_manager
        self.delivery_manager = delivery_manager
        self.current_time = 0  # Track the simulation time
        self.time_step = time_step  # Time step in hours

    def advance_time(self):
        self.current_time += self.time_step
        self.update_truck_locations()
        self.update_package_statuses()

    def update_truck_locations(self):
        for truck in self.truck_manager.trucks:
            # Calculate the distance traveled based on time_step and speed
            distance_traveled = truck.average_speed * self.time_step
            truck.drive_to(distance_traveled)
            # Update truck's location and other relevant details

    def update_package_statuses(self):
        for truck in self.truck_manager.trucks:
            for package_id in truck.package_list:
                package = self.delivery_manager.get_package(package_id)
                # Update package status based on truck location, delivery deadlines, etc.

    def get_package_status(self, package_id):
        package = self.delivery_manager.get_package(package_id)
        return package.status

    def get_truck_status(self, truck_id):
        for truck in self.truck_manager.trucks:
            if truck.truck_id == truck_id:
                return truck.miles_driven, truck.package_list
        return None