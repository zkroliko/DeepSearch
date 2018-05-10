from acoAlgorithm.Field import Field, FieldType
from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.TwoCoordinate import TwoCoordinate

import numpy as np


class Move:
    # Do we have self stepping enabled
    CAN_STAND = False

    def __init__(self, start, end):
        self.source = start
        self.target = end

    def valid(self, area):
        # Standing not allowed
        standing = self.source == self.target
        result = not standing and area.is_field_accessible(self.target)
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

    def __str__(self):
        return "%s->%s" % (self.source, self.target)

    def __eq__(self, other):
        return self.source == other.source and self.target == other.target

    def __hash__(self):
        return hash(hash(self.source) - hash(self.target))
