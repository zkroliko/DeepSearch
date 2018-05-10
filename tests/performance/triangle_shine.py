import time

from acoAlgorithm.Point import Point
from acoAlgorithm.View import ViewGenerator
from examples.Scenario1 import Scenario1
from examples.Scenario3 import Scenario3
from examples.Scenario4 import Scenario4

a = Scenario3.area()

start = time.clock()

for l in range(1):
    v = ViewGenerator(a)
    for i in range(a.main.start.x, a.main.end.x):
        for j in range(a.main.start.y, a.main.end.y):
            v.shine_from_triangles(Point(i, j))
            # print i*a.main.end.y+j

end = time.clock() - start

print "Triangle: %s and %s left" % (end, v.lm.area_to_discover)

start = time.clock()

for k in range(1):
    v = ViewGenerator(a)
    for i in range(a.main.start.x, a.main.end.x):
        for j in range(a.main.start.y, a.main.end.y):
            v.shine_from(Point(i, j))

end = time.clock() - start

print "Normal: %s and %s left" % (end, v.lm.area_to_discover)
