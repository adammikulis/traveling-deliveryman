# This class is deprecated due to poor performance/under-encapsulation and should be used for reference only

# from datetime import *
#
# class Greedy:
#     def __init__(self, graph_data_loader, package_data_loader, truck_manager):
#         self.graph_data_loader = graph_data_loader
#         self.graph = graph_data_loader.graph
#         self.package_data_loader = package_data_loader
#         self.package_hash_table = package_data_loader.package_hash_table
#
#         self.truck_manager = truck_manager
#         self.current_address_id = 0
#         self.package_id_list = self.package_hash_table.id_index
#         self.special_list_weight = 1 # Used to prioritize special packages
#
#     def load_special_package_lists(self):
#         # Load packages required by specific trucks
#         for truck_id, package_ids in self.package_data_loader.package_required_trucks.items():
#             for package_id in package_ids:
#                 if package_id in self.package_id_list:
#                     self.truck_manager.trucks[truck_id - 1].load_special_package_id_list(package_id)
#                     self.package_id_list.remove(package_id)
#
#         # Load grouped packages
#         for group_id, package_ids in self.package_data_loader.package_groups.items():
#             # Default to the third truck for grouped packages (lowest mileage so far)
#             for package_id in package_ids:
#                 package = self.package_hash_table.search(package_id)
#                 if package_id in self.package_id_list:
#                     self.truck_manager.trucks[1].load_special_package_id_list(package_id)
#                     self.package_id_list.remove(package_id) # Remove from global package id list
#
#     # The actual greedy algorithm
#     def sort_packages_onto_trucks(self):
#         # Assign package groups and required packages to their trucks
#         self.load_special_package_lists()
#
#         for truck in self.truck_manager.trucks:
#             while not truck.is_full() and (self.package_id_list or truck.special_package_id_list):
#
#                 if len(truck.special_package_id_list) + len(truck.package_id_list) == truck.max_packages:
#                     next_package_id, closest_distance = self.get_next_closest_package_id(truck, True)
#                     is_package_special = True
#                 # Use the method to get the package with the most urgent deadline and closest distance
#                 else:
#                     next_package_id, is_package_special = self.get_next_urgent_closest_package_id(truck)
#
#                 if next_package_id is not None:
#                     package = self.package_hash_table.search(next_package_id)
#                     package.truck_id = truck.truck_id
#                     truck.load_package(next_package_id)
#
#                     # Safely remove the package ID from the appropriate list
#                     if is_package_special and next_package_id in truck.special_package_id_list:
#                         truck.special_package_id_list.remove(next_package_id)
#                     elif next_package_id in self.package_id_list:
#                         self.package_id_list.remove(next_package_id)
#
#         for truck in self.truck_manager.trucks:
#             print(truck)
#
#     def get_next_urgent_closest_package_id(self, truck):
#         # Combine and prioritize packages based on deadline and distance
#         best_package_id = None
#         best_score = float('inf')
#         reference_time = datetime.combine(datetime.now().date(), time(8, 0))
#
#         # Combine both lists for assessment
#         combined_package_list = self.package_id_list + truck.special_package_id_list
#
#         for package_id in combined_package_list:
#             package = self.package_hash_table.search(package_id)
#             deadline_difference = (package.delivery_deadline - reference_time).total_seconds()  # Closer deadlines have lower score
#             deadline_score = abs(deadline_difference)
#             distance_score = self.graph_data_loader.get_direct_distance(self.current_address_id, package.address_id)
#
#             deadline_weight = 1
#             # Create a combined score, modify weights as needed
#             combined_score = (deadline_weight * deadline_score) + distance_score
#
#             if combined_score < best_score:
#                 best_score = combined_score
#                 best_package_id = package_id
#
#         is_package_special = best_package_id in truck.special_package_id_list
#         return best_package_id, is_package_special
#
#     # Searches through global regular list or truck's special package list depending on arg
#     def get_next_closest_package_id(self, truck, use_special_list=False):
#         closest_package_id = None
#         closest_distance = float('inf')
#         earliest_deadline = datetime.max
#
#         package_list = truck.special_package_id_list if use_special_list else self.package_id_list
#
#         for package_id in package_list:
#             package = self.package_hash_table.search(package_id)
#             deadline = package.delivery_deadline
#
#             # Calculate distance to the package
#             distance = self.graph.get_direct_distance(self.current_address_id, package.address_id)
#
#             # Prioritize by deadline, then by distance
#             if deadline < earliest_deadline or (deadline == earliest_deadline and distance < closest_distance):
#                 closest_distance = distance
#                 closest_package_id = package.package_id
#                 earliest_deadline = deadline
#
#         return closest_package_id, closest_distance
#
#     # Search through both special and regular package list, returning closest package and whether it is special or not
#     def get_next_combined_closest_package_id(self, truck):
#         closest_regular_package_id, closest_regular_distance = self.get_next_closest_package_id(truck, False)
#         closest_special_package_id, closest_special_distance = self.get_next_closest_package_id(truck, True)
#
#         # Logic to determine whether to choose a regular or special package
#         if closest_regular_package_id is None:
#             return closest_special_package_id, True
#         elif closest_special_package_id is None:
#             return closest_regular_package_id, False
#
#         if closest_regular_distance < closest_special_distance:
#             return closest_regular_package_id, False
#         else:
#             return closest_special_package_id, True
