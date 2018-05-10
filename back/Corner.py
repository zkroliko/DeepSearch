from enum import Enum

from acoAlgorithm.Field import Field, FieldType


# The offset is needed for raytracing
class CornerType(Enum):
    top_left = (-0.5, 0.5)
    top_right = (0.5, 0.5)
    bottom_left = (-0.5, -0.5)
    bottom_right = (0.5, -0.5)


# For representing corners
class Corner(Field):
    def __init__(self, x, y, type=FieldType.empty, rectangle=None, corner_type=None):
        Field.__init__(self, x, y, type, rectangle)
        self.corner_type = corner_type

    def is_corner(self):
        return True

    @staticmethod
    def good_coordinates(x, y):
        return True

    # Does this field, being a corner,
    # has any contact with rectangles in it's area
    def is_free_corner(self):
        if self.rectangle.area and self.is_corner():
            contact = self.rectangle.area.rectangles_in_contact(self.confine())
            return contact.__len__() is 1
        else:
            raise Exception("Must have an area set")

    # Same as before just diagonally
    def is_free_corner_diagonally(self):
        if self.rectangle.area and self.is_corner():
            try:
                # The following instructions check area for a fields of given coordinates
                to_check = []
                if self is self.rectangle.top_left:
                    f = self.rectangle.area.field(self.x - 1, self.y + 1)
                    if f:
                        to_check.append(f)
                if self is self.rectangle.top_right:
                    f = self.rectangle.area.field(self.x + 1, self.y + 1)
                    if f:
                        to_check.append(f)
                if self is self.rectangle.bottom_left:
                    f = self.rectangle.area.field(self.x - 1, self.y - 1)
                    if f:
                        to_check.append(f)
                if self is self.rectangle.bottom_right:
                    f = self.rectangle.area.field(self.x + 1, self.y - 1)
                    if f:
                        to_check.append(f)
            except Exception:  # Should be out of area or something
                return False
            # There mustn't be a field in the area
            # and if there is, then it must be the other type
            # normally we do this for occupied fields
            for tc in to_check:
                if tc is not None:
                    if tc is self.type:
                        return False

            return True

        else:
            raise Exception("Must have an area set")
