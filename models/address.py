class Address:

    def __init__(self, address_id, location_name, street_address, city, state, zip_code):
        self.address_id = address_id
        self.location_name = location_name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __str__(self):
        return f"{self.location_name} ({self.street_address}, {self.city}, {self.state} {self.zip_code})"
