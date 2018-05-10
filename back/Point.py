import numpy as np

from acoAlgorithm.Corner import Corner
from acoAlgorithm.Field import Field
from acoAlgorithm.TwoCoordinate import TwoCoordinate


class Point(TwoCoordinate):
    @staticmethod
    def map_to_point(argument):
        if isinstance(argument, Corner):
            return Point.corner_to_point(argument)
        elif isinstance(argument, Field):
            return Point.field_to_point(argument)

    @staticmethod
    def field_to_point(field):
        return Point(field.x, field.y)

    @staticmethod
    def corner_to_point(corner):
        return Point(corner.x + corner.corner_type.value[0], corner.y + corner.corner_type.value[1])

    def __init__(self, x, y):
        TwoCoordinate.__init__(self, x, y)
        self.origin = None
        self.angle = None

    def set_origin(self, point):
        self.origin = point
        self.__manage_radial()

    def __manage_radial(self):
        if self.origin:
            self.angle = self.__get_angle(self.origin)
            # Range is not important
            # self.range = dx*cos(self.angle)

    def __get_angle(self, origin):
        dx = self.x - origin.x
        dy = self.y - origin.y
        # Corner cases
        if dx == 0:
            return np.pi / 2 if dy > 0 else -np.pi / 2
        if dy == 0:
            return 0 if dx > 0 else np.pi
        # Normal
        if dx > 0:
            return np.arctan(dy / dx)
        else:
            return np.arctan(dy / dx) + np.pi

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __hash__(self):
        return hash(self.__str__())
