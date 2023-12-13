from models import ChainingHashTable
from models import DistanceTable
from models import Package
import random


class Greedy:
    def __init__(self, distance_data_loader, package_data_loader, truck_manager):
        random.seed(42)
        self.distance_data_loader = distance_data_loader
        self.distance_table = distance_data_loader.distance_table
        self.package_data_loader = package_data_loader
        self.package_hash_table = package_data_loader.package_hash_table

        self.truck_manager = truck_manager
        self.current_address_id = 0
        self.package_id_list = self.package_hash_table.package_id_index
        self.noise_factor = 0.00
        self.special_list_weight = 1 # Used to prioritize special packages

    def load_special_packages(self):

        # Load packages required by specific trucks
        for truck_id, package_ids in self.package_data_loader.package_required_trucks.items():
            for package_id in package_ids:
                if package_id in self.package_id_list:
                    self.truck_manager.trucks[truck_id - 1].load_special_package(package_id)
                    self.package_id_list.remove(package_id)

        # Load grouped packages
        for group_id, package_ids in self.package_data_loader.package_groups.items():
            # Default to the third truck for grouped packages (lowest mileage so far)
            for package_id in package_ids:
                package = self.package_hash_table.search(package_id)
                if package_id in self.package_id_list:
                    self.truck_manager.trucks[2].load_special_package(package_id)
                    self.package_id_list.remove(package_id) # Remove from global package id list

    def sort_packages_onto_trucks(self):
        self.load_special_packages()  # Loads special packages into their own lists in the trucks
        for truck in self.truck_manager.trucks:
            # Artificially restrict max packages to try optimization
            # if truck.truck_id == 1:
            #     truck.max_packages = 15
            # Break loop if truck is full or if the global package_id_list and truck's special_package_id_list are empty
            while not truck.is_full() and (self.package_id_list or truck.special_package_id_list):
                # Forces assignment from special_package_id_list when combined list total is at max_capacity
                if len(truck.package_id_list) + len(truck.special_package_id_list) == truck.max_packages:
                    next_package_id, next_package_distance = self.get_next_closest_package_id(truck, True)
                    truck.package_id_list.append(next_package_id)
                    truck.special_package_id_list.remove(next_package_id)
                    package = self.package_hash_table.search(next_package_id)
                    package.truck_id = truck.truck_id
                else:
                    next_package_id, is_package_special = self.get_next_combined_closest_package_id(truck)
                    package = self.package_hash_table.search(next_package_id)
                    package.truck_id = truck.truck_id
                    truck.load_package(next_package_id)
                    if is_package_special:
                        truck.special_package_id_list.remove(next_package_id)
                    else:
                        self.package_id_list.remove(next_package_id)
            print(truck)


    # Searches through global regular list or truck's special package list depending on arg
    def get_next_closest_package_id(self, truck, use_special_list=False):
        closest_distance = float('inf')
        closest_package_id = None

        # Choose the appropriate list based on the use_special_list flag
        package_list = truck.special_package_id_list if use_special_list else self.package_id_list

        for package_id in package_list:
            noise_weight = 1 + random.uniform(-self.noise_factor, self.noise_factor)
            package = self.package_hash_table.search(package_id)
            distance = self.distance_table.get_distance(self.current_address_id, package.address_id) * noise_weight
            if distance < closest_distance:
                closest_distance = distance
                closest_package_id = package.package_id

        return closest_package_id, closest_distance

    # Search through both special and regular package list, returning closest package and whether it is special or not
    def get_next_combined_closest_package_id(self, truck):
        closest_regular_package_id, closest_regular_distance = self.get_next_closest_package_id(truck, False)
        closest_special_package_id, closest_special_distance = self.get_next_closest_package_id(truck, True)

        # Check if both lists are empty
        if closest_regular_package_id is None and closest_special_package_id is None:
            return None

        # Check if one of the lists is empty and return the package from the non-empty list
        if closest_regular_package_id is None:
            return closest_special_package_id, True
        elif closest_special_package_id is None:
            return closest_regular_package_id, False

        # If both lists have packages, choose the package with the shortest distance
        if closest_regular_distance is not None and (closest_special_distance is None or closest_regular_distance < closest_special_distance * self.special_list_weight):
            return closest_regular_package_id, False
        else:
            return closest_special_package_id, True