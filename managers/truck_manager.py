from models import Truck

class TruckManager:

    def __init__(self, total_trucks, algorithm, package_data_loader, max_packages=16, average_speed=18):
        self.trucks = [Truck(truck_id=i + 1, algorithm=algorithm, package_data_loader=package_data_loader, max_packages=max_packages, average_speed=average_speed) for i in range(total_trucks)]