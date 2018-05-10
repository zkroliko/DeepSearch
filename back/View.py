import itertools
from multiprocessing.pool import Pool

import multiprocessing
import numpy as np

from acoAlgorithm.Point import Point
from acoAlgorithm.LightMap import LightMap
from acoAlgorithm.Ray import Ray
from acoAlgorithm.utils.TriangleArea import triangle_area
from acoAlgorithm.utils.TriangleRasterization import rasterize_triangle


class ViewGenerator():
    # Used for heuristic of using triangles for raytracing
    MIN_TRIANGLE_AREA = 5

    NUMBER_OF_STRIPES = 1

    def __init__(self, area, shadow_map=None):
        self.visited = {}
        self.area = area
        self.lm = LightMap(area, shadow_map)
        # For triangle raytracing
        # self.corner_points = []
        # self.setup_corners()

    # Adds possible moves to light map
    def react_to_new_place(self, moves):
        # The place in which the walker currently is
        self.lm.look_around_at((moves[0].source.x, moves[0].source.y))
        # The rest -> if you can move there, you can see it
        # for move in moves:
        #     self.lm.check((move.target.x, move.target.y))

    def shine_onto_stripe(self, source, start, end):
        for i in range(start, end + 1):
            for j in range(self.area.main.start.y, self.area.main.end.y + 1):
                self.__shine_directly(source, i, j)

    def __shine_directly(self, source, x, y):
        if self.lm.remains_to_be_checked((x, y)):
            if Ray(source, Point(x, y), area=self.area).valid():
                self.lm.look_around_at((x, y))

    def setup_corners(self):
        # Make points from corners
        corners = list(itertools.chain(*map(lambda x: x.free_corners(), self.area.all_rectangles())))
        for c in corners:
            point = Point.corner_to_point(c)
            self.corner_points.append(point)
        # Area borders
        for c in self.area.main.corners():
            point = Point.corner_to_point(c)
            self.corner_points.append(point)

    def __shine_with_rectangle(self, source, x, y):
        if self.lm.remains_to_be_checked((x, y)):
            ray = Ray(source, Point(x, y), area=self.area)
            shell = ray.rectangle_shell()
            possible_rectangles = self.area.rectangles_in_contact(shell)
            if possible_rectangles:
                for rectangle in possible_rectangles:
                    if ray.collides(rectangle):
                        return
                # Checked all the rectangles that might coincide and none is present
                self.lm.look_around_at((x, y))
            else:
                for raw_field in shell.all_fields_raw():
                    self.lm.look_around_at(raw_field)

    def shine_from_triangles(self, source):
        # Make points from corners
        visible = [x for x in self.corner_points if Ray(source, x, area=self.area).valid()]

        # Sorting
        sorted_vis = ViewGenerator.sorted_to_origin(visible, source)
        # We have to change it into an array
        source_array = [source.x, source.y]
        for i in range(len(sorted_vis)):
            first = [sorted_vis[i].x, sorted_vis[i].y]
            second = [sorted_vis[(i + 1) % (len(sorted_vis))].x, sorted_vis[(i + 1) % (len(sorted_vis))].y]
            # Making a triangle
            triangle = np.array([source_array, first, second])
            # Heuristic checking whether it will be fruitful to rasterize
            if triangle_area(source_array, first, second) < self.MIN_TRIANGLE_AREA:
                return 0
            # Retrieving fields in np.array
            try:
                fields = rasterize_triangle(triangle)
                if len(fields) > 0:
                    self.add_raw_fields(fields)
                    return len(fields)
            except (ValueError):
                pass  # todo: This algorithm has some uncovered corner cases, remove the clause when it doesn't

    def add_raw_fields(self, fields):
        for entry in fields:
            if 0 <= entry[0] <= self.area.main.end.x and 0 <= entry[1] <= self.area.main.end.y:
                self.lm.look_around_at((entry[0], entry[1]))

    @staticmethod
    def sorted_to_origin(points, origin):
        # Make points origin for all corners
        for point in points:
            point.set_origin(origin)

        return sorted(points, key=lambda x: x.angle)
