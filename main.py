from models.truck import Truck
from models import Package
from models import ChainingHashTable

from controllers import DataLoaders


if __name__ == '__main__':

    package_hash_table = ChainingHashTable(40)
    package_data_loader = DataLoaders(package_hash_table)

    package_data_filepath = "data/package_data.csv"
    package_data_loader.load_package_data(package_data_filepath)

    print(package_hash_table.table)