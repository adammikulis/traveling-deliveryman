from models import Truck

class TruckManager:

    def __init__(self, total_trucks, distance_data_loader, package_data_loader):
        self.trucks = [Truck(distance_data_loader, package_data_loader, truck_id=i+1) for i in range(total_trucks)]