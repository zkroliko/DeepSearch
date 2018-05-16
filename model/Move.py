from model.field import Field, FieldType
from model.rectangle import Rectangle
from model.twoCoordinate import TwoCoordinate

import numpy as np


class Move:
    def __init__(self, start, end=None, vector=None):
        self.source = start
        if end:
            self.target = end
            self.vector = (end.x-start.x,end.y-start.y)
        elif vector:
            self.vector = vector
            self.target = Field(start.x + vector[0], start.y + vector[1])

    def valid(self, area):
        result = area.is_field_accessible(self.target)
        return result

    @staticmethod
    def target_accessible(self, area):
        # General test for exiting the area
        if self.target not in area.main:
            return False
        # All other cases
        rect = area.rectangle_of(self.target.x, self.target.y)
        # Everything ok
        if rect:
            if rect.type != FieldType.inaccessible:
                return True
            else:
                return False
        return True

    def __str__(self):
        return "%s->%s" % (self.source, self.target)

    def __eq__(self, other):
        return self.source == other.source and self.target == other.target

    def __hash__(self):
        return hash(hash(self.source) - hash(self.target))
