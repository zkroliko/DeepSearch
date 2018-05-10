import time

from acoAlgorithm.LightMap import LightMap
from acoAlgorithm.LightMapOld import LightMapOld
from acoAlgorithm.Point import Point
from acoAlgorithm.View import ViewGenerator
from examples.Scenario1 import Scenario1
from examples.Scenario2 import Scenario2
from examples.Scenario3 import Scenario3
from examples.Scenario4 import Scenario4

a = Scenario3.area()

def test(lightMap, shadowMap):
    v = ViewGenerator(a)

    start = time.clock()

    for k in range(10):

        v.lm = lightMap(a,shadowMap)
        for i in range(a.main.start.x, a.main.end.x):
            for j in range(a.main.start.y, a.main.end.y):
                v.lm.look_around_at((i, j))

        for i in range(a.main.start.x, a.main.end.x):
            for j in range(a.main.start.y, a.main.end.y):
                v.lm.remains_to_be_checked((i, j))

    end = time.clock() - start

    print("Full: %s" % end)

    start = time.clock()

    for l in range(10):
        v = ViewGenerator(a)
        v.lm = lightMap(a,shadowMap)
        for i in range(a.main.start.x, a.main.end.x):
            for j in range(a.main.start.y, a.main.end.y):
                v.lm.remains_to_be_checked((i, j))

    end = time.clock() - start

    print("Empty: %s" % end)

print("New")
test(LightMap, LightMap.build_shadow_map(a))
print("Old")
test(LightMapOld, None)