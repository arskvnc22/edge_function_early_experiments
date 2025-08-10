class MiniHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size  # initialize empty table with fixed size
    def _hash(self, key):
        return hash(key) % self.size  # get index in table
    def insert(self, key, value):
        index = self._hash(key)
        original_index = index
        steps = 0

        while self.table[index] is not None:
            existing_key, _ = self.table[index]
            if existing_key == key:
                # Key already exists → update value
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.size
            steps += 1
            if steps >= self.size:
                raise Exception("Hash table is full")

        self.table[index] = (key, value)

    def get(self, key):
        index = self._hash(key)
        steps = 0

        while self.table[index] is not None:
            existing_key, value = self.table[index]
            if existing_key == key:
                return value
            index = (index + 1) % self.size
            steps += 1
            if steps >= self.size:
                break

        return None  # not found


        
ht = MiniHashTable()

ht.insert("apple", 42)
ht.insert("banana", 99)

print(ht.get("apple"))   # → 42
print(ht.get("banana"))  # → 99
print(ht.get("orange"))  # → None
