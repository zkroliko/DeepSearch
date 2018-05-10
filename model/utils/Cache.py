
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.elements = {}
        self.lru = {}

    def has(self, key):
        return key in self.elements

    def get(self, key):
        if key in self.elements:
            self.lru[key] = self.size
            self.size += 1
            return self.elements[key]
        return None

    def set(self, key, value):
        if len(self.elements) >= self.capacity:
            # Find the LRU entry
            old_key = min(self.lru.keys(), key=lambda k: self.lru[k])
            self.elements.pop(old_key)
            self.lru.pop(old_key)
        self.elements[key] = value
        self.lru[key] = self.size
        self.size += 1


class MoveCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.elements = {}
        self.lru = {}

    def has(self, move):
        return self.make_set(move) in self.elements

    def get(self, move):
        move_set = self.make_set(move)
        if move_set in self.elements:
            self.lru[move_set] = self.size
            self.size += 1
            return self.elements[move_set]
        return None

    def set(self, move, value):
        if len(self.elements) >= self.capacity:
            # Find the LRU entry
            old_key = min(self.lru.keys(), key=lambda k: self.lru[k])
            self.elements.pop(old_key)
            self.lru.pop(old_key)
        move_set = self.make_set(move)
        self.elements[move_set] = value
        self.lru[move_set] = self.size
        self.size += 1

    @staticmethod
    def make_set(move):
        return frozenset([move.source, move.target])
