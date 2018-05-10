import random
import time

from acoAlgorithm.LightMap import LightMap
from acoAlgorithm.LightMapOld import LightMapOld
from acoAlgorithm.Point import Point
from acoAlgorithm.View import ViewGenerator
from examples.Scenario1 import Scenario1
from examples.Scenario2 import Scenario2
from examples.Scenario3 import Scenario3
from examples.Scenario4 import Scenario4

a = Scenario2.area()

start = time.clock()

sm = LightMap.build_shadow_map(a)

for i in range(100):
    start2 = time.clock()
    lm = LightMap(a,sm)
    for j in range(50):
        x, y = random.randint(0,a.main.width()-1), random.randint(0,a.main.height()-1)
        lm.look_around_at((x,y))
    print(time.clock() - start2)

print("total", time.clock() - start)