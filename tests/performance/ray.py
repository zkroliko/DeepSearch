import time

from acoAlgorithm.Field import Field
from acoAlgorithm.Point import Point
from acoAlgorithm.Ray import Ray
from acoAlgorithm.Rectangle import Rectangle
from tests.rayTest import TestRay

start = time.time()

for i in range(0,300):
        ray = Ray(Point(2, 2), Point(20, 20))
        test_cases = {
            Rectangle(Field(0, 5), Field(3, 5)): False,
            Rectangle(Field(0, 5), Field(2, 6)): False,
            Rectangle(Field(0, 2), Field(2, 3)): True,
            Rectangle(Field(0, 3), Field(3, 4)): True,
            Rectangle(Field(0, 3), Field(2, 3)): False,
            Rectangle(Field(2, 0), Field(3, 2)): True,
            Rectangle(Field(5, 0), Field(8, 5)): True,
            Rectangle(Field(0, 0), Field(24, 24)): True,
            Rectangle(Field(8, 8), Field(24, 24)): True,
            Rectangle(Field(22, 22), Field(24, 24)): False,
            Rectangle(Field(0, 5), Field(6, 5)): True,
            Rectangle(Field(0, 0), Field(4, 4)): True,
            Rectangle(Field(3, 3), Field(4, 4)): True,
            Rectangle(Field(3, 3), Field(5, 5)): True,
            Rectangle(Field(0, 6), Field(8, 8)): True
        }

        for rectangle, result in test_cases.iteritems():
            ray.collides(rectangle)


end = time.time() - start

print end

