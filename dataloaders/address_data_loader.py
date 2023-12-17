import csv

from models import Address
# This class loads the csv with address information to match to address id
class AddressDataLoader:

    def __init__(self):
        self.address_table = {}

    def load_address_data(self, file_name):
        with open(file_name) as Addresses:
            address_data = csv.reader(Addresses)
            next(address_data) # skips header
            for address in address_data:
                address_id = int(address[0])
                location_name = address[1]
                street_address = address[2]
                city = address[3]
                state = address[4]
                zip_code = int(address[5])

                address_object = Address(address_id, location_name, street_address, city, state, zip_code)

                self.add_address(address_object)

    def add_address(self, address):
        self.address_table[address.address_id] = address

    def get_address(self, address_id):
        return self.address_table.get(address_id)