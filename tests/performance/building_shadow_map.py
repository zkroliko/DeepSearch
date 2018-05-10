import time

from model.LightMap import LightMap
from model.LightMapOld import LightMapOld
from model.Point import Point
from model.View import ViewGenerator
from examples.Scenario1 import Scenario1
from examples.Scenario2 import Scenario2
from examples.Scenario3 import Scenario3
from examples.Scenario4 import Scenario4

a = Scenario2.area()

start = time.clock()


for i in range(10):
    start2 = time.clock()
    sm = LightMap.build_shadow_map(a)
    print(time.clock() - start2)

print("total", time.clock() - start)