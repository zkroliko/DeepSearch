import numpy as np

from model.point import Point
from model.ray import Ray


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

    def look_around_at(self, position):
        """Updates the "seen" area with the part visible from position
        :param position: Field at which we like the Walker to look around
        """
        was_seen = self.is_checked(position)
        self.to_discover = self.shadow_map_with_new_position(position)
        return not self.is_checked(position)

    def shadow_map_with_new_position(self, position):
        """Returns a ndarray which is would be the current "visited" are after moving to the position
        :param position: Field from which we would like the Walker to potentially to look around
        """
        coordinates = (position.x, position.y)
        to_remove = np.logical_and(self.to_discover, self.shadow_map[coordinates])
        return np.logical_xor(self.to_discover, to_remove)

    def remains_to_be_checked(self, position):
        return self.to_discover[(position.x, position.y)]

    def is_checked(self, position):
        return not self.remains_to_be_checked(position)

    def finished(self):
        return np.sum(self.to_discover) <= 0

    def how_many_left(self):
        return np.sum(self.to_discover)
