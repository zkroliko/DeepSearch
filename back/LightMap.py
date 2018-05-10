from enum import Enum

import bitarray as bitarray
import numpy as np

from acoAlgorithm.Point import Point
from acoAlgorithm.Ray import Ray


class LightMap:
    def __init__(self, area, shadow_map=None):
        # Total area
        self.area = area
        self.shadow_map = shadow_map if shadow_map else LightMap.build_shadow_map(area)
        total_area = area.main.size()
        self.to_discover = np.ones((area.main.width(), area.main.height()), dtype=bool)

        # Removing occupied areas, they don't need to be discovered
        occupied = []
        for item in area.all_rectangles():
            if item.type:
                occupied.append(item)
        # Mapping to sizes
        sizes = map(lambda x: x.size(), occupied)
        occupied_area = sum(sizes)

        # Checking out occupied area
        for rect in occupied:
            for coordinates in rect.all_fields_raw():
                self.to_discover[coordinates[0], coordinates[1]] = False

    @staticmethod
    def build_shadow_map(area):
        map = {}
        for x in range(area.main.width()):
            for y in range(area.main.height()):
                # We might have found ourself inside a rectangle
                if not area.rectangle_of(x, y):
                    map[(x, y)] = LightMap._visibility_map_for_point(Point(x, y), area)
                else:
                    map[(x, y)] = np.zeros((area.main.width(), area.main.height()), dtype=bool)
        return map

    @staticmethod
    def _visibility_map_for_point(source, area):
        visible = np.zeros((area.main.width(), area.main.height()), dtype=bool)
        for x in range(area.main.width()):
            for y in range(area.main.height()):
                visible[x, y] = True if Ray(source, Point(x, y), area=area).valid() else False
        return visible

    def look_around_at(self, coordinates):
        was_seen = self.is_checked(coordinates)
        to_remove = np.logical_and(self.to_discover, self.shadow_map[coordinates])
        self.to_discover = np.logical_xor(self.to_discover, to_remove)
        return not was_seen

    def remains_to_be_checked(self, coordinates):
        return self.to_discover[coordinates[0], coordinates[1]]

    def is_checked(self, coordinates):
        return not self.remains_to_be_checked(coordinates)

    def finished(self):
        return np.sum(self.to_discover) <= 0

    def how_many_left(self):
        return np.sum(self.to_discover)
