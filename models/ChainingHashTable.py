class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts new item into hash table
    def insert(self, key, item):
        # Get bucket list where item will be added
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for item with matching key in hash table
    def search(self, key):
        # Get bucket list where the key will be
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None

    # Removes item with matching key from hash table
    def remove(self, key):
        # Get bucket list where item will be removed
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove([key_value[0], key_value[1]])


myHash = ChainingHashTable()
myHash.insert(1, "package 1")
myHash.insert(2, "package 2")

print(myHash.search("package 1"))
print(myHash.table)
