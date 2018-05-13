import itertools
from multiprocessing.pool import Pool

import multiprocessing
import numpy as np

from model.point import Point
from model.lightMap import LightMap
from model.ray import Ray
from model.utils.TriangleArea import triangle_area
from model.utils.TriangleRasterization import rasterize_triangle


class EmptyView():

    def __init__(self, area):
        self.area = area

    def finished(self):
        return True

    def react_to_new_place(self, moves):
        pass

    def shine_onto_stripe(self, source, start, end):
        pass

    def __shine_directly(self, source, x, y):
        pass

    def setup_corners(self):
        pass

    def __shine_with_rectangle(self, source, x, y):
        pass

    def shine_from_triangles(self, source):
        pass

    def add_raw_fields(self, fields):
        pass

    @staticmethod
    def sorted_to_origin(points, origin):
        pass