class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts new item into hash table
    def insert(self, item):
        # Get bucket list where item will be added
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

        bucket_list.append(item)

    # Searches for item with matching key in hash table
    def search(self, key):
        # Get bucket list where the key will be
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None

    # Removes item with matching key from hash table
    def remove(self, key):
        # Get bucket list where item will be removed
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)


myHash = ChainingHashTable()
myHash.insert("Adam")
myHash.insert("Ruthy")

print(myHash.search("Adam"))
print(myHash.search("Nothing"))
print(myHash.table)
