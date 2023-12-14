
# Code modified from Webinar 1: Let's Get Hashing
class ChainingHashTable:
    def __init__(self, initial_capacity):
        self.table = [[] for i in range(initial_capacity)]
        self.package_id_index = []

    # Inserts new item into hash graph
    def insert(self, key, item):
        if key not in self.package_id_index:
            self.package_id_index.append(key)

        # Get bucket list where item will be added
        bucket = hash(key) % len(self.table)  # Use key for hashing rather than item for consistency
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for item with matching key in hash graph
    def search(self, key):
        # Get bucket list where the key will be
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None

    # Removes item with matching key from hash graph
    def remove(self, key):
        # Get bucket list where item will be removed
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove(key_value)  # Remove the key-value pair directly
                return True
        return False

