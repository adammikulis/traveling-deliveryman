from models import Truck

class TruckManager:

    def __init__(self, total_trucks):
        self.trucks = [Truck(truck_id=i+1) for i in range(total_trucks)]

    def load_package_into_truck(self, package_id, truck_id):
        if truck_id <= len(self.trucks):
            self.trucks[truck_id - 1].load_package(package_id)
        else:
            print("No truck with that id")

    def unload_package_from_truck(self, package_id, truck_id):
        if truck_id <= len(self.trucks):
            self.trucks[truck_id - 1].unload_package(package_id)
        else:
            print("No truck with that id")