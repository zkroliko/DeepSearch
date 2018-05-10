import copy

from enum import Enum

from acoAlgorithm.TwoCoordinate import TwoCoordinate


# Used for distinguishing empty and inaccessible fields
class FieldType(Enum):
    empty = 0
    inaccessible = 1


class Field(TwoCoordinate):
    # The type is empty on default
    # If the field is just a hypothetical field or a small rectangle,
    # then it will create it's own rectangle
    def __init__(self, x, y, type=FieldType.empty, rectangle=None):
        if not self.good_coordinates(x, y):
            raise Exception("The coordinates cannot be negative")
        TwoCoordinate.__init__(self, x, y)
        # Setting the type, default is empty
        self.type = type
        self.rectangle = rectangle

    @staticmethod
    def good_coordinates(x, y):
        if x < 0 or y < 0:
            return False
        else:
            return True

    # Is this field a corner in it's rectangle
    def is_corner(self):
        return False

    # See the rectangle method confine(self)
    def confine(self):
        # We are using copy because the new rectangle is just a tool
        from acoAlgorithm.Rectangle import Rectangle
        return Rectangle(copy.copy(self), copy.copy(self)).confine()

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)
