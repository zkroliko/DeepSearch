import hashlib

from acoAlgorithm.Corner import Corner, CornerType
from acoAlgorithm.Field import FieldType, Field

import numpy as np

# Rectangle is identified by two fields at the end of it's diagonal
from acoAlgorithm.Point import Point
from acoAlgorithm.TwoCoordinate import TwoCoordinate


class Rectangle():
    def __init__(self, start, end, type=FieldType.empty, area=None):
        self.type = type

        # The start and end should
        # be chosen so the start goes up and right to end
        # in clearer words vector [start,end] should be positive

        self.start = Corner(min(start.x, end.x), min(start.y, end.y), corner_type=CornerType.bottom_left,
                            rectangle=self)
        self.end = Corner(max(start.x, end.x), max(start.y, end.y), corner_type=CornerType.top_right, rectangle=self)

        self.start.rectangle = self
        self.end.rectangle = self
        # For other corners
        self.top_left = Corner(self.start.x, self.end.y, self.type, self, corner_type=CornerType.top_left)
        self.top_right = self.end
        self.bottom_left = self.start
        self.bottom_right = Corner(self.end.x, self.start.y, self.type, self, corner_type=CornerType.bottom_right)

        if area is not None:
            self.area = area.get_root()
            self.area += self
        else:
            self.area = None

    # Returns corners in COUNTERCLOCKWISE order from the corner self.start
    def corners(self):
        return [self.start, self.bottom_right, self.end, self.top_left]

    # Returns all the corners having
    # any contact with rectangles in it's area
    def free_corners(self):
        return [c for c in self.corners() if c.is_free_corner()]

    # This actually creates a Field object
    # which is a part of the rectangle
    # at given coordinates
    def field(self, x, y):
        return Field(x, y, self.type, rectangle=self)

    # Is the item contained in self
    def __contains__(self, item):
        # Duck type yourself, no way to do this logically
        # with proper abstraction
        if isinstance(item, TwoCoordinate):
            return self.contains_two_coord(item)
        elif isinstance(item, Rectangle):
            return self.contains_rectangle(item)

    def contains_two_coord(self, item):
        # Concise version is not used because of performance
        # whole things should be inline but can't because this is python
        # return self.end >= item >= self.start
        return self.end.x >= item.x >= self.start.x and self.end.y >= item.y >= self.start.y

    def contains_rectangle(self, item):
        return self.end >= item.end and self.start <= item.start

    def contains_inside(self, item):
        # Duck type yourself, no way to do this logically
        # with proper abstraction
        if isinstance(item, TwoCoordinate):
            return self.contains_two_coord_inside(item)
        elif isinstance(item, Rectangle):
            return self.contains_rectangle_inside(item)

    def contains_two_coord_inside(self, item):
        # Concise version is not used because of performance
        # whole things should be inline but can't because this is python
        # return self.end > item > self.start
        return self.end.x > item.x > self.start.x and self.end.y > item.y > self.start.y


    def contains_rectangle_inside(self, item):
        return self.end > item.end and self.start < item.start

    def width(self):
        return self.end.x - self.start.x + 1

    def height(self):
        return self.end.y - self.start.y + 1

    def size(self):
        return self.width() * self.height()

    # Returns a point which is the middle of the rectangle
    def middle(self):
        mid_x = (self.start.x + self.end.x) // 2
        mid_y = (self.start.y + self.end.y) // 2
        # Parity of dimensions, sorry for unclarity, the best way
        x_adjust = (self.width() + 1) % 2
        y_adjust = (self.width() + 1) % 2

        if x_adjust + y_adjust == 0:
            return Field(mid_x, mid_y, type=self.type)
        else:
            return Rectangle(Field(mid_x, mid_y), Field(mid_x + 1, mid_y + 1), type=self.type)

    # Logical operator and
    # Will return None or a rectangle if there is an intersection
    def __and__(self, other):
        # This is THE MOST IMPORTANT short circuit
        # covers 95% of cases
        if self.start > other.end or other.start > self.end:
            return None

        # We will start by checking the corners of both figures
        # First lets check if self is fully contained in other
        self_inside_other = [c for c in self.corners() if other.contains_two_coord(c)]

        if len(self_inside_other) == 4:
            return self

        # Other way around
        other_inside_self = [c for c in other.corners() if self.contains_two_coord(c)]
        if len(other_inside_self) == 4:
            return other

        # Maybe there is no intersection
        if len(other_inside_self) + len(self_inside_other) == 0:
            return None
        # Now lengths of count_other and count_self are (0,2), (1,1) or (2,0)

        # Points of intersection

        # We will use both or one, depending on the number of intersections

        if len(self_inside_other) == 1:
            intersection = Field(max(self.start.x, other.start.x), max(self.start.y, other.start.y))
            second_intersection = Field(min(self.end.x, other.end.x), min(self.end.y, other.end.y))
            return Rectangle(intersection, second_intersection, self.type)
        else:
            # This is for the case when whole
            # side of one rectangle is contained the other
            # we have to know which is which
            if len(self_inside_other) == 2:
                points_inside = self_inside_other
                outer_rectangle = self
                inner_rectangle = other
            else:
                points_inside = other_inside_self
                outer_rectangle = other
                inner_rectangle = self

        # We have to ensure that we pick the "broader" rectangle

        inside_point1 = points_inside[0]
        inside_point2 = points_inside[1]

        # Checking whether intersection is vertical or horizontal
        # We only have to know one intersection

        if inside_point1.x == inside_point2.x:  # Vertical
            if inner_rectangle.start.x > outer_rectangle.start.x:
                intersection = Field(inner_rectangle.start.x, inside_point1.y)
            else:
                intersection = Field(inner_rectangle.end.x, inside_point1.y)
        else:  # Horizontal
            if inner_rectangle.start.y > outer_rectangle.start.y:
                intersection = Field(inside_point1.x, inner_rectangle.start.y)
            else:
                intersection = Field(inside_point1.x, inner_rectangle.end.y)

        # The wrong one has one of the coordinates the same as the other
        if inside_point1.x == intersection.x or inside_point1.y == intersection.y:
            return Rectangle(intersection, inside_point2, self.type)
        else:
            return Rectangle(intersection, inside_point1, self.type)

    # Boolean version of above method
    def has_intersection(self, other):
        # We will start by checking the corners of both figures
        for c in self.corners():
            if other.contains_two_coord(c):
                return True

        # Other way around
        for c in other.corners():
            if self.contains_two_coord(c):
                return True

        return False

    def confine(self):
        if self.area:
            start = Field(max(self.area.main.start.x, self.start.x - 1), max(self.area.main.start.y, self.start.y - 1))
            end = Field(min(self.area.main.end.x, self.end.x + 1), min(self.area.main.end.y, self.end.y + 1))
        else:
            start = Field(max(0, self.start.x - 1), max(0, self.start.y - 1))
            end = Field(self.end.x + 1, self.end.y + 1)

        return Rectangle(start, end, type=self.type, area=None)

    # Is this rectangle in contact with other rectangle
    def is_in_contact(self, other):
        return self.confine() & other is not None

        # BEWARE, THIS IS ANTISYMMETRIC !!! DOESN'T MAKE much SENS FOR NOW, BUT I NEED THIS

    # Return the rectangle being the contact "area" with other rectangle
    def contact(self, other):
        if isinstance(other, Rectangle):
            # We need to know which one is smaller
            # If they are of equal size it doesn't matter
            if self.size() > other.size():
                bigger_one = self
                smaller_one = other
            else:
                bigger_one = other
                smaller_one = self
            # Now we check the confine of the smaller one
            return smaller_one.confine() & bigger_one
        elif isinstance(other, Field):
            return self.contact(other.rectangle)
        else:
            raise Exception("Unsupported operation with: ", type(other))

    # Is the contact with other rectangle diagonal
    def is_in_contact_diagonal(self, other):
        # This should cover all cases
        contact = self.contact(other)
        return contact is not None and contact.size() == 1

    # Is the contact with other rectangle vertical or horizontal
    def is_in_contact_v_h(self, other):
        # This should cover all cases
        contact = self.contact(other)
        return contact is not None and contact.size() > 1

    # Can we join these two rectangles
    def is_joinable(self, other):
        # Could be one big logic expression but it would be ugly
        # 1. Areas have to match or the join must be taking place
        # in a hypothetical space without areas but they
        # cannot overlap
        # 2. Generally other has to be a rectangle
        # and in vertical or horizontal contact with self
        if isinstance(other, Rectangle) and self & other is None \
                and (self.area == other.area or self & other is None) \
                and self.is_in_contact_v_h(other) \
                and self.type == other.type:
            # Other than that their dimensions and contact size have to match
            contact = self.contact(other)
            # Special case for two 1xn or nx1 rectangles
            if self.size() != other.size():
                if smaller(self, other) == bigger(self, other).confine() & smaller(self, other):
                    return False
            # Normal case
            return self.width() == other.width() == contact.width() or \
                   self.height() == other.height() == contact.height()
        else:
            return False

    # Joining the rectangles, uses is_joinable to check first
    def join(self, other):
        if self.is_joinable(other):
            corners = self.corners().__add__(other.corners())
            corners.sort(key=lambda f: (f.x, f.y), reverse=False)
            start = corners.pop(0)
            corners.reverse()
            end = corners.pop(0)
            result = Rectangle(start, end, type=self.type, area=None)
            a = self.area
            if a is not None:
                a -= self
                a -= other
                a += result
            return result
        else:
            raise Exception("Rectangles are not joinable")

    def all_fields_raw(self):
        result = []
        for i in range(self.start.x, self.end.x + 1):
            for j in range(self.start.y, self.end.y + 1):
                result.append((i, j))
        return result

    # Used for raytracing
    def corner_shell(self):
        start = Point.map_to_point(self.bottom_left)
        end = Point.map_to_point(self.top_right)
        return Rectangle(start, end)

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return self.start == other.start and self.end == other.end and self.type == other.type
        elif isinstance(other, Field):
            return self == other.rectangle

    def __str__(self):
        return "%s\t...\t%s\n" \
               "...\t\t...\t\t...\n" \
               "%s\t...\t%s" % (self.top_left, self.top_right, self.bottom_left, self.bottom_right)

    def __hash__(self):
        return hash("%s%s%s" % (self.start, self.end, self.type))

def bigger(first, second):
    if isinstance(first, Rectangle) and isinstance(second, Rectangle):
        if first.size() > second.size():
            return first
        else:
            return second
    else:
        return None


def smaller(first, second):
    if isinstance(first, Rectangle) and isinstance(second, Rectangle):
        if first.size() > second.size():
            return second
        else:
            return first
    else:
        return None
