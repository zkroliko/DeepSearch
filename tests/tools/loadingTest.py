import unittest

from model.area import Area
from model.field import Field
from model.rectangle import Rectangle
from model.tools.Loader import load_from_file


class TestLoading(unittest.TestCase):

    # Only run manually
    def test_simple(self):
        dim = 64

        a = Area(Rectangle(Field(0, 0), Field(dim-1, dim-1)), 1)

        load_from_file("../maps/4", a, 'x')
        pass
