import math

from acoAlgorithm.Field import Field
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.TwoCoordFloat import TwoCoordFloat
from acoAlgorithm.TwoCoordinate import TwoCoordinate

import numpy as np

from acoAlgorithm.utils.FloatUtils import is_close


class Ray:
    def __init__(self, start, end, area=None):
        self.start = start
        self.end = end
        self.area = area

    def rectangle_shell(self):
        start = Field(int(math.floor(self.start.x)), int(math.floor(self.start.y)))
        end = Field(int(math.ceil(self.end.x)), int(math.ceil(self.end.y)))
        return Rectangle(start, end)

    def valid(self):
        possible_rectangles = self.area.rectangles_in_contact(self.rectangle_shell())
        for rectangle in possible_rectangles:
            if self.collides(rectangle):
                return False
        # Checked all the rectangles that might coincide
        return True

    def in_x_space(self, x):
        start = min(self.start.x, self.end.x)
        end = max(self.start.x, self.end.x)
        equal = is_close(self.start.x, x) or is_close(self.end.x, x)
        return start < x < end or equal

    def in_y_space(self, y):
        start = min(self.start.y, self.end.y)
        end = max(self.start.y, self.end.y)
        equal = is_close(self.start.y, y) or is_close(self.end.y, y)
        return start < y < end or equal

    def collides(self, rect):
        # TODO: Revamp this probably
        # This needed because of how the coordinates are set up
        rect = rect.corner_shell()

        # A corner case which isn't covered in later algorithm
        if rect.contains_two_coord_inside(self.start) or rect.contains_two_coord_inside(self.end):
            return True

        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        # Corner case todo: Make sure it is correct
        if is_close(dx, 0):
            if rect.start.x <= self.start.x <= rect.end.x:
                for corner in rect.corners():
                    if self.in_y_space(corner.y):
                        return True
            return False
        elif is_close(dy, 0):
            if rect.start.y <= self.start.y <= rect.end.y:
                for corner in rect.corners():
                    if self.in_x_space(corner.x):
                        return True
            return False
        else:
            # Normal case
            a = float(dy) / float(dx)
            b = -a * self.start.x + self.start.y
            collisions = 0
            contact_points = 0

            for corner in rect.corners():
                # -- One way around
                if self.in_x_space(corner.x):
                    # So it has the plausible x
                    x = corner.x
                    y = a * x + b
                    # Let's check the y
                    if not self.in_y_space(y):
                        # Simply cannot be
                        continue
                    # So it has the plausible x and y
                    mapped_x = TwoCoordFloat(x, y)
                else:
                    mapped_x = None

                # -- Other way around
                if self.in_y_space(corner.y):
                    # So it has a plausible y
                    y = corner.y
                    x = (y - b) / float(a)
                    # Let's check the x
                    if not self.in_x_space(x):
                        # Simply cannot be
                        continue
                    # So it has the plausible x and y
                    mapped_y = TwoCoordFloat(x, y)
                else:
                    mapped_y = None

                maps_to_x = True if mapped_x and rect.contains_two_coord(mapped_x) else False
                maps_to_y = True if mapped_y and rect.contains_two_coord(mapped_y) else False

                if maps_to_x or maps_to_y:
                    collisions += 1
                    if mapped_x and mapped_y and mapped_x == mapped_y:
                        contact_points += 1
            if contact_points > 1:
                return True
            elif collisions > 2:
                if collisions == 3 and contact_points == 1:
                    return False
                else:
                    return True
            else:
                return False

    def __str__(self):
        return "%s-%s" % (self.start, self.end)
