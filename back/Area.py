from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field, FieldType


class Area:
    # Soo...
    # We don't really need two types of fields
    # so the area may contain fields of one type
    # and we must know which ones
    IS_SINGLE_TYPE = True
    EXISTING_TYPE = FieldType.inaccessible

    # Creates an area's recursively
    # If resolution is > 1 then it will create children
    # Main is a rectangle that contains all rectangles in the area, specifies dimensions
    # Main size must be 2^n.
    def __init__(self, main, resolution=1, parent=None):
        if isinstance(main, Rectangle):
            if main.height() == main.width() and is_power2(main.height()):
                self.main = main
                self.parent = parent
                self.resolution = resolution
                # Subindexes
                if resolution > 1:
                    self.top_left = Area(
                        Rectangle(self.main.top_left, self.main.middle().top_left), resolution - 1, self)
                    self.top_right = Area(
                        Rectangle(self.main.middle().top_right, self.main.top_right), resolution - 1, self)
                    self.bottom_left = Area(
                        Rectangle(self.main.bottom_left, self.main.middle().bottom_left), resolution - 1, self)
                    self.bottom_right = Area(
                        Rectangle(self.main.bottom_right, self.main.middle().bottom_right), resolution - 1, self)
                    self.children = [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
                self.rectangles = []

    @staticmethod
    def of_size(size):
        return Area(Rectangle(Field(0, 0), Field(size - 1, size - 1)))

    # Or does it have children
    def is_subindexed(self):
        return self.resolution > 1

    def width(self):
        return self.main.width()

    def height(self):
        return self.main.height()

    # Recursively finds root of the whole index
    def get_root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()

    # Adds a rectangle to the index
    def __iadd__(self, other):
        if isinstance(other, list):
            for rectangle in other:
                self.__add_one(rectangle)
        else:
            self.__add_one(other)
        return self

    def __add_one(self, item):
        if isinstance(item, Rectangle):
            # Checking if it fits in our area
            # this will be done recursively
            if self.main & item:
                if self.is_subindexed():
                    for child in self.children:
                        child += item
                else:
                    for r in self.rectangles:
                        if r & item is not None:
                            raise Exception("The rectangle coincides current rectangles")
                    # Ok
                    item.area = self.get_root()
                    self.rectangles.append(item)

    # Removes a rectangle from the index
    def __isub__(self, other):
        if isinstance(other, Rectangle):
            # Checking if it fits in our area
            # this will be done recursively
            # this is ensured by iadd method
            if other & self.main:  # TODO: Different than iadd
                if other in self.rectangles:
                    self.rectangles.remove(other)
                if self.is_subindexed():
                    for child in self.children:
                        child -= other
        return self

    # Clear's the whole area from rectangles
    def clear(self):
        # Checking if it fits in our area
        # this will be done recursively
        # this is ensured by iadd method
        self.rectangles = []  # New array
        if self.is_subindexed():
            for child in self.children:
                child.clear()

    # Does this area contain a rectangle or field
    # DISPUTABLE SPECIFICATION
    def __contains__(self, item):
        if isinstance(item, Rectangle):
            return self.main & item is not None
        if isinstance(item, Field):  # TODO: Why?
            return item in self.main

    # Gets a given field from area
    def field(self, x, y):
        target = Field(x, y)
        if target in self:
            if self.is_subindexed():
                for child in self.children:
                    found = child.field(x, y)
                    if found is not None:
                        return found
            else:
                for r in self.rectangles:
                    if target in r:
                        return r.field(x, y)
        return None

    # Gets all rectangles coinciding with a given rectangle
    def rectangles_in_contact(self, target):
        result = set()
        if self.is_subindexed():
            for child in self.children:
                result.update(child.rectangles_in_contact(target))
        else:
            for r in self.rectangles:
                if target.has_intersection(r):
                    result.add(r)
        return result

    # Gets a rectangle covering a given field
    def rectangle_of(self, x, y):
        target = Field(x, y)
        # First let's check if it's in the area at all
        if target in self:
            if self.is_subindexed():
                for child in self.children:
                    found = child.rectangle_of(x, y)
                    if found is not None:
                        return found
            else:
                for r in self.rectangles:
                    if target in r:
                        r.area = self.get_root()
                        return r
        elif self.resolution != 1:
            # We've got phony coordinates
            raise Exception("Target is outside the area")
        return None

    # Returns all unique rectangles in the area
    def all_rectangles(self):
        all = set()
        if self.is_subindexed():
            for child in self.children:
                all.update((child.all_rectangles()))
        else:
            for r in self.rectangles:
                all.add(r)
        # Unique
        return all

    def is_field_accessible(self, target):
            # General test for exiting the area
            if target not in self.main:
                return False
            # All other cases
            rect = self.rectangle_of(target.x, target.y)
            # Everything ok
            if rect:
                if rect.type == FieldType.empty:
                    return True
                else:
                    return False
            # So we got none
            # That can mean that there only one type
            # in the map, if it's inaccessible then we are ok
            # because we are on empty field
            if self.IS_SINGLE_TYPE and self.EXISTING_TYPE == FieldType.inaccessible:
                return True
            else:
                return False


def is_power2(num):
    # states if a number is a power of two
    return ((num & (num - 1)) == 0) and num != 0
