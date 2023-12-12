class Driver:

    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.assigned_truck_id = 0

    def set_assigned_truck_id(self, truck_id):
        self.assigned_truck_id = truck_id