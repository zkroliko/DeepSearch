class TwoCoordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Duplication is the shortest
    # Could be changes to comparing tuples
    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __lt__(self, other):
        return not (self.__ge__(other))

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x ^ self.y)
