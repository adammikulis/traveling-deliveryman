from models import Truck

class TruckManager:

    def __init__(self, total_trucks):
        self.trucks = [Truck(truck_id=i+1) for i in range(total_trucks)]